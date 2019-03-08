### ClientCodeCrawler.py
```ClientCodeCrawler.py``` downloads client code files importing a target API from popular GitHub repositories (i.e., with most stars).

###### Arguments

| Argument | DESCRIPTION |EXAMPLE|
| ------ | ------ | ------ |
| -a, --api | Target API | javax.xml.transform |
| -o, --out_dir| Output Directory | /User/xxx/data/javax_xml_transform/ |
| -t, --token| Github Access Token | a9w6ew6w3a45w49weww4e8w3swwh3v1s5a9m42e |
| -ow | Set to Overwrite Existing Files | . |

###### Example
```sh
python ClientCodeCrawler.py -a javax.xml.transform -o /User/xxx/data/javax_xml_transform/ -t a9w6ew6w3a45w49weww4e8w3swwh3v1s5a9m42e -ow

