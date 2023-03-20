# django-simple-vite

A simple Django app to integrate Vite.js easily in your Django project.


## Install:

```
pip install django-simple-vite
```

Then add `simple_vite` to `INSTALLED_APPS` in Django settings.

```
INSTALLED_APPS = [
    ...
    'simple_vite',
    ...
]
```

## Settings:

During development, set `VITE_SERVER_URL` in Django settings, pointing to the Vite.js development server, e.g.:

```
VITE_SERVER_URL = 'http://localhost:3000'
```

When in production, you don't need to set `VITE_SERVER_URL`, because the compiled assets produced by Vite.js will be served as regular static files.

## Usage:
------

Create an app that will contain your Vite.js powered frontend:

```
./manage.py startapp frontend
```

Inside your app, create a `vite_src` directory (the name is arbitrary). This directory will contain your Javascript sources, that will be compiled by Vite.js.

In the `vite_src` directory, create a `vite.config.js` file, with this content:

```
const { resolve } = require('path');

export default {
    build: {
        manifest: true, // adds a manifest.json
        rollupOptions: {
            input: [
              // Use main.js file as entrypoint for your JS app.
              resolve(__dirname, './main.js'),
            ]
        },
        // Puts the Vite.js manifest.json in
        // PROJECT_ROOT/frontend/static/
        outDir:  '../static',
        // puts compiled asset files (js, css) in
        // PROJECT_ROOT/frontend/static/frontend
        assetsDir:  'frontend',
    },
    plugins: [],
    server: {
        // This port should match with VITE_SERVER_URL Django setting.
        port: 3000,
        open: false,
    }
};
```

In the `vite_src` directory, create a `main.js` file, that will serve as entry point for your app, with this content:

```
// Add this at the beginning of your app entry.
import 'vite/modulepreload-polyfill';
import 'main.css';

console.log("hello world");
```

`main.css` is a CSS file that will be imported by Vite and used by your application.

Install Vite.js in your `vite_src` directory:

```
yarn add vite
```

Add a couple of script in your `package.json`:

```
{
  "dependencies": {
    "vite": "^4.1.4"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  }
}
```

Launch Vite.js server:

```
yarn dev
```

Create a Django template `index.html` that will hold the HTML markup used by your application, save it inside your `frontend` Django app in a subdirectory `templates/frontend/`.

```
{% load vite %}

<html>
<head>
    {% vite_styles 'main.js' %}
</head>
<body>
    <h1>Hello world</h1>

    {% vite_scripts 'main.js' %}
</body>

</html>
```

Now create a view in your frontend app that will serve the template above:

```
from django.views.generic import TemplateView

class ViteView(TemplateView):
    template_name = 'frontend/index.html'
```

Now mount the view in a URLConf for the app. Create a `urls.py` file in your `frontend` app directory with this content:

```
from django.urls import path

from . import views

app_name = 'frontend'
urlpatterns = [
    path('', views.ViteView.as_view(), name='home'),
]
```

And finally include the `frontend` URLconf in your main project urls:

```
from django.urls import path
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]
```

Now, if you visit the root of your Django webapp (usually on http://localhost:8000), you'll see a basic Vite.js powered web app.
Keep your Vite.js server running (see `yarn dev` above), and you'll have Hot Module Replacement (HMR) enabled!
