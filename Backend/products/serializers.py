from rest_framework import serializers
from .models import Product
from rest_framework.reverse import reverse
from .validators import validate_title 
from api.serializers import UserPublicSerializer


class ProductSerializer(serializers.ModelSerializer):
    owner=UserPublicSerializer(source='user',read_only=True)
    my_user_data=serializers.SerializerMethodField(read_only=True)
    my_discount=serializers.SerializerMethodField(read_only=True)
    # url=serializers.SerializerMethodField(read_only=True)
    edit_url=serializers.SerializerMethodField(read_only=True)
    url=serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field="pk"
    )


    title=serializers.CharField(validators=[validate_title])

    class Meta:
        model=Product
        fields=['id',
                'owner',
                'my_user_data',
                'title',
                'content',
                'price',
                'sale_price',
                'my_discount',
                'url',
                'edit_url',
                ]
        
    def get_my_user_data(self,obj):
        return {
            "username":obj.user.username
        }

    def create(self, validated_data):
        # email=validated_data.pop('email')
        content= validated_data.get("content")
        if content is None:
            validated_data['content']=validated_data.get('title')
        
        return super().create(validated_data)


    def update(self, instance, validated_data):
        if Product.objects.exclude(pk=instance.pk).filter(title=validated_data.get('title')).exists():
            
            raise serializers.ValidationError({"Validation Error":"product title already exists"})
        else:
            print('*1'*20)
            print(validated_data)
            print(instance)
            if 'content' not in validated_data or validated_data.get('content') =='' :
                print('*2'*20)
                print(validated_data)
                print(instance)

                validated_data['content']=validated_data.get('title')
                print('*3'*20)

                print(validated_data)
                print(instance)

                instance.content=validated_data.get('content',instance.content)
            print('*4'*20)

            print(validated_data)
            print(instance)
            instance.save()
            return instance
            

    def get_my_discount(self,obj):
        return obj.get_discount()

    # def validate_title(self,value):
    #     qs=Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    

    # def get_url(self,obj):
    #     # return f"/api/products/{obj.id}"
    #     request=self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("product-detail", kwargs={'pk':obj.id},request=request)
    
    def get_edit_url(self,obj):
        request=self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={'pk':obj.id},request=request)