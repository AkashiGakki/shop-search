## `Django` 项目最佳实践

### 初始化

#### 创建虚拟环境

- 虚拟环境生成

```shell
mkdir nono && cd nono
pipenv install 
ls
```

- 修改 `pipenv` 源

```shell
vim Pipfile
```

修改 `url` 为 `https://mirrors.aliyun.com/pypi/simple`

- 激活虚拟环境

```shell
pipenv shell
```

#### 创建 `Django` 项目

- 安装 `Django`

```shell
pipenv install django --skip-lock
```

- 生成项目

```shell
django-admin startproject nono .
```

#### 应用

- 创建应用

```shell
mkdir apps
python manage.py startapp shop
mv -f shop apps/
```

修改 `apps.py`:

```python
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.shop'
```

直接手动移动应用到 `apps` 目录下，`app.py` 可以自动同步，不需要手动修改

- 添加应用名到 `setting.py` 中的 `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.shop.apps.ShopConfig',    
]
```

#### 模型

- 数据库配置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shopbop',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

安装包

```shell
pipenv install mysqlclient
```

- 创建模型

```python
from django.db import models

class Shop(models.Model):
    pass
```

- 激活模型

```python
python manage.py makemigrations
```

- 迁移并同步数据库

```python
python manage.py migrate
```

#### 视图

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, akashi!')
```

#### 路由

- 项目层路由

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('apps.shop.urls'))
]
```

- 应用层路由

```python
from django.urls import path

from apps.shop.views import ShopListView

urlpatterns = [
    path('index', views.index, name='index'),
]
```

#### 启动服务

```python
python manage.py runserver
```

#### 简单项目重构

##### 改良 `URLconf`

- 项目路由

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('apps.shop.urls', namespace='shop'))
]
```

- 应用路由

```python
from django.urls import path

from apps.shop import views
from apps.shop.views import ShopListView

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('list', ShopListView.as_view(), name='shop-list'),
]
```

##### 改良视图

```python
import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View

from apps.shop.models import Shop


class ShopListView(View):
    def get(self, request):
        queryset = Shop.objects.all()
        data = serializers.serialize('json', queryset)
        return JsonResponse(json.loads(data), safe=False)
```

目前模型里面还没有数据，所以访问 `http://127.0.0.1:8000/shop/list` 会返回一个空数组，但现在其实已经实现了数据的序列化返回

下面再从 `Admin` 中添加数据以后就可以查询到数据了

#### 额外配置

##### `Admin` 模块

- 创建一个超级管理员账号

```python
python manage.py createsuperuser
```

```
Username: akashi
Email address:(选填)
Password: akashiadmin123
```

- 将模型注册到 `admin` 

`admin.py`:

```python
from django.contrib import admin
from apps.shop.models import Shop

admin.site.register(Shop)
```

- 登录管理页面进行后台管理

重新启动项目，访问 `http://127.0.0.1:8000/admin/`

添加数据之后，可以通过 `http://127.0.0.1:8000/shop/list` 查询

##### 语言和时间配置

`setting.py`:

```python
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False
```

#### `restframework`

- 安装

```python
pipenv install coreapi
pipenv install pygments
pipenv install django-guardian
pipenv install djangorestframework
pipenv install markdown       # Markdown support for the browsable API.
pipenv install django-filter  # Filtering support
```

`Add 'rest_framework' to your INSTALLED_APPS setting.`

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

`urls.py`:

```python
urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

- 定义序列化模型

新建 `serializer.py` 存放序列化模型

```python
from rest_framework import serializers

from apps.shop.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
```

- 重写视图函数

重写 `views.py`:

```python
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from apps.shop.models import Shop
from apps.shop.serializer import ShopSerializer


class ShopViewSet(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
```

- 定义新路由

```python
from django.urls import path
from rest_framework import routers

from apps.shop import views
from apps.shop.views import ShopListView
from apps.shop.views import ShopViewSet


app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('list', ShopListView.as_view(), name='list'),
    path('view', ShopViewSet.as_view(), name='view')
]
```

或者使用 `restframework` 提供的 `routers`:

```python
from django.urls import path, include
from rest_framework import routers

from apps.shop import views
from apps.shop.views import ShopListView
from apps.shop.views import ShopViewSet


app_name = 'shop'
router = routers.DefaultRouter()
router.register('view', ShopViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('list', ShopListView.as_view(), name='list'),
    path('', include(router.urls)),
]
```

但是这样，`ShopViewSet` 必须继承自 `mixins.ListModelMixin, viewsets.GenericViewSet`

```python
from rest_framework import viewsets, mixins

from apps.shop.models import Shop
from apps.shop.serializer import ShopSerializer


class ShopViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
```

序列化完成之后，就只差数据了，我这里选择将爬取的 `mongodb` 里面的数据导入到项目的 `mysql` 数据库中

- 从 `mongodb` 导出

```shell
mongoexport -d shopbop -c tmall -f _id,keyword,good_url,image_url,price,describe,shop,shop_url --type=csv -o /Users/mac/Source/Files/Project/Python_Django/nono/tmall.csv
```

- 定义模型 `Tmall`

```python
class Tmall(models.Model):
    _id = models.CharField(max_length=200, primary_key=True)
    keyword = models.CharField(max_length=10)
    goods_url = models.URLField()
    image_url = models.URLField()
    goods_price = models.CharField(max_length=10)
    describe = models.TextField(max_length=500)
    shop = models.CharField(max_length=50)
    shop_url = models.URLField()

    def __str__(self):
        return self.keyword
```

- 激活模型并迁移数据库

```shell
python manage.py makemigrations
python manage.py migrate
```

- 导入数据到 `mysql`

```shell
load data infile "/Users/mac/Source/Files/Project/Python_Django/nono/tmall.csv"
replace into table shop_tmall 
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n';
```

```shell
load data infile "/tmp/tmall.csv"
replace into table shop_tmall 
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n';
```

执行指令如果出现 `ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement` 在 `mysql` 中查询：

```shell
show variables like '%secure%';
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| require_secure_transport | OFF   |
| secure_file_priv         | NULL  |
+--------------------------+-------+
2 rows in set (0.01 sec)
```

我们需要将 `secure_file_priv` 修改为空(`""`)

如果使用 `Mac` 的 `HomeBrew` 安装 `MySQL`，可以在目录

`/usr/local/etc/my.cnf`

找到文件，修改为 `secure_file_priv=""`

- 序列化模型

```python
from rest_framework import serializers

from apps.shop.models import Shop, Tmall


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class TmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tmall
        fields = '__all__'
```

- 视图函数

```python
class TmallViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tmall.objects.all()
    serializer_class = TmallSerializer
```

- 路由

```python
from django.urls import path, include
from rest_framework import routers

from apps.shop import views
from apps.shop.views import ShopListView, TmallViewSet
from apps.shop.views import ShopViewSet


app_name = 'shop'

router = routers.DefaultRouter()
router.register('view', ShopViewSet)
router.register('tmall', TmallViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('list', ShopListView.as_view(), name='list'),
    path('', include(router.urls)),
]
```

##### 分页

```python
from rest_framework.pagination import PageNumberPagination

class TmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_description = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class TmallViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tmall.objects.all()
    serializer_class = TmallSerializer
    pagination_class = TmallPagination

```

##### 搜索

```python
class TmallViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tmall.objects.all()
    serializer_class = TmallSerializer
    pagination_class = TmallPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['keyword', 'describe', 'shop']
```

##### 排序

```python
class TmallViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tmall.objects.all()
    serializer_class = TmallSerializer
    pagination_class = TmallPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['keyword', 'describe', 'shop']
    ordering_fields = ['sold_num', 'add_time']
```

当然，需要设置字段 `sold_num` 和 `add_time`



