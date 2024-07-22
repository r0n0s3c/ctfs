## This Message will self destruct

This service can generate message link that will self-destruct. BTW, Which SPY movie do you like? 😎

It seems like a python app with the following packages:
python = "^3.10"
werkzeug = "2.2.3"
flask = "2.2.3"
pillow = "^10.1.0"
mysql-connector-python = "^8.3.0"
uwsgi = "^2.0.23"
flask-wtf = "^1.2.1"
requests = "^2.31.0"


Files that matter:


Methods:
- `@app.get('/')`
- `@app.post('/')`
    - Get `id`, `password` and `file` or `image_url` parameter
    - Validate form
      - If we use the image_url a GET request is made and the content of the response is saved. M
    - Add image to the database
- `@app.get('/trial')`
    - Creates a URL containing the TRIAL_IMAGE with `secrets.token_urlsafe(32)` as the password
- `@app.get('/<id>')`
    - Uses the id to get an image from the database
    - If it finds, get the image content `open(os.path.join(FILE_SAVE_PATH, id+'-mosaic')`
    - use `image_data2url()` to set the base64 image
    - Set a timer, and then run `delete_image()` to delete the image
- `@app.post('/<id>')`
    - Uses the id to get an image from the database
    - If it finds, verify if its the same password
    - If its the same password, get the content file from `open(os.path.join(FILE_SAVE_PATH, id)`
    - use `image_data2url()` to set the base64 image

Solution:

Endpoints `@app.post('/<id>')` and `@app.get('/<id>')` do not have a vulnerability.
Endpoint `@app.get('/trial')` seems like to have a flag in the blur image. It uses a function called `__add_image()` to add the image into the filesystem:

```py

@app.get('/trial')
def trial():
    with open(TRIAL_IMAGE, 'rb') as f:
        file = FileStorage(stream=f, content_type='image/png')
        url = __add_image(
            secrets.token_urlsafe(32),
            uuid4().hex,
            file=file,
            admin=True
        )
    return jsonify({'url': url})
``` 

Inside the function it uses a separate thread to run a function called `convert_and_save()`.
If the function call comes from other endpoint instead of the `/trial` we will wait 5 seconds and in the end add to the db. 


```py
def __add_image(password, id_, file=None, image_url=None, admin=False):
    t = Thread(target=convert_and_save, args=(id_, file, image_url))
    t.start()

    # no need, but time to waiting heavy response makes me excited!!
    if not admin:
        time.sleep(5)

    if file:
        mimetype = file.content_type
    elif image_url.endswith('.jpg'):
        mimetype = 'image/jpg'
    else:
        mimetype = 'image/png'

    db.add_image(id_, mimetype, password)

    return urljoin(URLBASE, id_)
```

Since we can know the id of the trial, we can try to overwrite by adding the same id with a new password however it gives an error since the id is primary key in the table. The convert_and_image has a error exception that if any error arise it will delete the id from db however we have another function call for the delete of the id of 


- Request trial
- Get the id of the trial
- Browse to the trial image, it will trigger the delete once the destruction_seconds have passed but the image will stay in the file system browsable using the same id.
- In order to not overwrite the image but add the id with the password to the database we create a python server that loops through the redirects because of `res = requests.get(url, timeout=3)` which creates a timeout every time there is a redirect.
- Since it runs on a different thread the `db.add_image(id_, mimetype, password)` will run and add the id to the db with our pass(the FLAG image is in the file system with the same id still).





self destruct does not delete the image from the disk, and if you hang the http request for new image with same id for 6 seconds you have 1 second window to get the image with your password before it gets overwritten with the uploaded image