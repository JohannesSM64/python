import subprocess, re

for i in re.findall('(http://blip.+)\[/url\]',
                    open('day9post.txt').read()):
    subprocess.call(["movgrab", i])
