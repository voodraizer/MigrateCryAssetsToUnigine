# Migrate CryEngine assets to Unigine

Предназначен для автоматического переноса ассетов (fbx, tif, префабов и уровней) из проекта на Cryengine в проект на Unigine.  
Текстуры и их каналы при переносе меняются согласно требованиям материалов Unigine PBR.  
В Unigine создаются соответствующие ассеты (модели, текстуры, материалы, префабы) и настраиватюся дефолтными или близкими к тем, что у них были в проекте CryEngine.  

### Python
Python 3.7   
Для экспорта текстур, материалов.   
Python 3.3   
Данная версия требуется для fbx sdk. Только для экспорта fbх моделек.

### Python FBX SDK
Скачать FBX Python SDK с [ОфСайта](https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0)    
Установку и справку по API можно почитать в [ОфДоках](http://download.autodesk.com/us/fbx/20112/FBX_SDK_HELP/index.html?url=WS1a9193826455f5ff453265c9125faa23bbb5fe8.htm,topicNumber=d0e8312)

### Pillow
Для работы с текстурами используется библиотека [Pillow](https://python-pillow.org/).   
Краткое описание и установку можно почитать в [ОфДоках](https://pillow.readthedocs.io/en/stable/installation.html).    

### Wand (устаревшее)
Для работы с текстурами используется библиотека [Wand](https://github.com/emcconville/wand/).  
Краткое описание и установку можно почитать в [ОфДоках](http://docs.wand-py.org/en/0.5.9/).    


```
Tips
   

```
