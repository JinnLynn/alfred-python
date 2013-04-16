# Alfred Python

A simple python module for alfred workflow。

Features:

* Easily get bundle id, query arguments 
* Simple feedback XML generation
* Provides functions for storing or retrieving cache data
* Workflow configuration management
* Includes an easy way to download remote file

## Code Example

```python
>>> import alfred
>>> alfred.bundleID()
'net.jeeker.awf.AppDig'
>>> alfred.log('log message')      # save log message to 'log.txt' in workflow's folder
>>> alfred.exit('exit-message')
exit-message
>>> alfred.exitWithFeedback(title='exitWithFeedback')
<items><item uid="net.jeeker.awf.AppDig.29008681"><icon>icon.png</icon><subtitle /><title>exitWithFeedback</title></item></items>

>>> feedback = alfred.Feedback()
>>> feedback.addItem(title='Feedback Title', subtitle='subtitle', autocomplete='subcmd', valid=False)
>>> feedback.addItem(title='Feedback Title 2', subtitle='subtitle 2', arg='arg')
>>> feedback.addItem(title='Feedback Title 3', subtitle='subtitle 3')
>>> feedback.output()
<items><item autocomplete="subcmd" uid="net.jeeker.awf.AppDig.11134445" valid="no"><icon>icon.png</icon><subtitle>subtitle</subtitle><title>Feedback Title</title></item><item arg="arg" uid="net.jeeker.awf.AppDig.20583908"><icon>icon.png</icon><subtitle>subtitle 2</subtitle><title>Feedback Title 2</title></item><item uid="net.jeeker.awf.AppDig.31032116"><icon>icon.png</icon><subtitle>subtitle 3</subtitle><title>Feedback Title 3</title></item></items>

>>> alfred.config.set(username='JinnLynn', testkey='testvalue')
>>> alfred.config.getAll()
{u'username': u'JinnLynn', u'testkey': u'testvalue'}
>>> alfred.config.get('username')
u'JinnLynn'
>>> alfred.config.delete('username')
>>> alfred.config.getAll()
{u'testkey': u'testvalue'}

>>> alfred.cache.set('test-cache', {'cache-data':'test-data'}, expire=10)
>>> alfred.cache.get('test-cache')
{u'cache-data': u'test-data'}
>>> alfred.cache.timeout('test-cache')
2.6863911151885986
>>> alfred.cache.get('test-cache')      # expired return None
>>> alfred.cache.timeout('test-cache')
-1

>>> alfred.storage.getLocalIfExists('http://i.imgur.com/17lNrSX.png')     # Non-existent
>>> alfred.storage.getLocalIfExists('http://i.imgur.com/17lNrSX.png', download=True)
'/tmp/net.jeeker.awf.AppDig/0fef92118c683242f9b6e2a40e1a54f5.png'
>>> alfred.storage.batchDownload(['http://i.imgur.com/8pa4x95.png','http://i.imgur.com/PX03uFm.png'])
>>> alfred.storage.getLocalIfExists('http://i.imgur.com/8pa4x95.png')
'/tmp/net.jeeker.awf.AppDig/dc119234ccb1f8fea4064b9a83a2dd6b.png'
```

## License
The MIT License