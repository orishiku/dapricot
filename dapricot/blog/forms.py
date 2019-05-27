from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import Comment, Commenter

class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = '__all__'
        
class CommenterForm(ModelForm):
    
    class Meta:
        model = Commenter
        fields = '__all__'
        
class CommentCommenterForm(forms.Form):
    nickname = forms.CharField(label='Nombre',max_length=50)
    email = forms.EmailField(label='Correo', max_length=50)
    content = forms.CharField(label='Comentario',max_length=500,widget=forms.widgets.Textarea())
    
    def get_or_create_comment_commenter(self, post):
        #commenter = None
        try:
            commenter = Commenter.objects.get(nickname=self.data['nickname'],
                                              email=self.data['email'])
            self.save_comment(commenter, post)
            return commenter, True
            
        except Commenter.DoesNotExist:            
            name = self.cleaned_data['nickname'].lower()
            
            if name.find("orishiku") < 0:
                try: 
                    commenter = Commenter(nickname=self.data['nickname'],
                                          email=self.data['email'])
                    commenter.save()
                    self._save_comment(commenter, post)
                    return commenter, True
                    
                except:
                    self.add_error(None, ValidationError(
                        mark_safe("El nickname o el correo ya se encuentran " +
                            "registrados. <a>¿No recuerdas tu nickname?</a>")))
                    
            else:
                self.add_error(None, ValidationError("Los usuarios no puede " +
                                  "contener la palabra 'ORISHIKU' o 'ADMIN' " +
                                  "en sus nombres."))
                print(self.non_field_errors()) 
        
        return None, False
    
    def _save_comment(self, commenter, post):
        comment = Comment(content=self.data['content'],
                          author=commenter,
                          post=post)
        
        if commenter.status == 'v':
            comment.status = 'a'
            
        comment.save()
        
        