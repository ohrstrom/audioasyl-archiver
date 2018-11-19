

```python
import codecs
import json
from pprint import pprint


with codecs.open('./dump.js', 'r', 'utf-8') as f:
    data = json.load(f)


for b in data:
    print(b['title'])
    print('num. prog:', len(b['programs']))
    print('---')



pprint(data[0]['programs'][0])


```
