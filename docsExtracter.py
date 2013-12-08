import sys
from pprint import pprint
from bs4 import BeautifulSoup,Tag


def createSOUPforMethod(methodObj,methodSpan,ignoreDesc = False):
    # signature and description
    if ignoreDesc or methodObj['desc'] == "":
        htmlStart = '<h3 data-name="{2}">{0}<span class="type">{1}</span></h3>'.format(methodObj['signature'],methodSpan,methodObj['name'])
    else:
        htmlStart = '<h3 data-name="{3}">{0}<span class="type">{1}</span></h3><p>{2}</p>'.format(methodObj['signature'],methodSpan,methodObj['desc'],methodObj['name'])


    #returns
    if 'returns' in methodObj:
        htmlStart += '<p>{0}</p>'.format(methodObj['returns']['title'])
        htmlStart += '<p>{0}</p>'.format(methodObj['returns']['desc'])
    
    # python code
    if 'pycode' in methodObj:
        htmlStart+= '<span class="code-header">code:</span>'
        htmlStart+= '<script type="syntaxhighlighter" class="brush: python"><![CDATA[{0}]]></script>'.format(methodObj['pycode'])

    #python output
    if 'pyoutput' in methodObj:
        htmlStart+= '<span class="code-header">output:</span>'
        htmlStart+= '<script type="syntaxhighlighter" class="brush: python"><![CDATA[{0}]]></script>'.format(methodObj['pyoutput'])

    #create soup
    retSOUP = BeautifulSoup(htmlStart,"html.parser")
    
    #arguments
    for argumentsTitle, argList in methodObj['arguments'].items():
        retSOUP.append(BeautifulSoup('<h4>{0}</h4'.format(argumentsTitle),"html.parser"))

        added = False
        argsTable = BeautifulSoup('<table></table>',"html.parser").table
        for arg in argList:
            argsTable.append(BeautifulSoup('<tr><th><b>{0}</b>{1}<br/></th><td>{2}</td></tr>'.format(
                arg['argName'],
                arg['argType'],
                arg['argDesc']),"html.parser"))
            added = True

        if added:
            retSOUP.append(argsTable)
        
    return retSOUP
        
            
def addToDict(dictObj,name,obj):
    if name in dictObj:
        dictObj[name].append(obj)
    else:
        dictObj[name] = [obj]

def has_sig(tag):
    return tag.select('spag.sig') != None


def returnsFilter(item):
    return item.string.startswith('Returns:')
    
def nextSiblingsFilter(item):
    return item != "\n"
    
def codeFilter(outputList):
    def filterFunc(item):
        if item in outputList:
            return False
        if item == '>>> ':
            return False
        return True
    return filterFunc



def docForFile(filename,className):

    soup = BeautifulSoup(open(filename))

    classDoc = {}


    # add class description

    classDoc['title'] = className

    classDoc['desc'] = soup.select('p')[1].string

    for table in soup.select('table.details'):
        sig = table.select('span.sig')
        if sig == []:
            continue
        sig = sig[0]
        #print(sig)

        methodObj = {}

        methodSignature = "".join(sig.stripped_strings).strip()

        # get description
        methodDesc = "".join(map(lambda p: p.string,table.select("p")))

        methodObj['signature'] = methodSignature
        methodObj['desc'] = methodDesc

        #method just name
        methodName = methodObj['signature'][0:methodObj['signature'].index("(")]
        methodObj['name'] = methodName
        
        #method class (method/class method/constructor)
        methodType = table.select('em.fname')

        if len(methodType) > 0:
            methodType = methodType[0]
            methodTypeStr = methodType.string
        else:
            methodTypeStr = "method"

    
        #python code
        pyCode = table.select('pre.py-doctest')

        if len(pyCode) > 0:
            pyCode = pyCode[0]
            # python output
            pyOutput = map(lambda item: item.string,pyCode.select('span.py-output'))
            # filter output from code
            pyCodeStr = "".join(filter(codeFilter(pyOutput),pyCode.strings))
            pyOutputStr =  "".join(pyOutput)
            methodObj['pycode'] = pyCodeStr
            methodObj['pyoutput'] = pyOutputStr

        #arguments
        methodObj['arguments'] = {}
        args = table.select('dl.fields')
    
        if args == []:
            continue

        #default arguments type is parameters
        argumentType = "Parametars:"
    
        args = args[0]

        for arg in args.select('li'):
            argString = "".join(arg.stripped_strings).strip()
            
            # check for category change
            p = arg.select('p')

            if len(p) > 0:
                p = p[0]
                argumentType = p.string
                argString = argString[0:argString.index(p.string)]
            
            argParts = argString.split("-")
            parenOpenIndex = argParts[0].index("(")
            parenCloseIndex = argParts[0].index(")")
            argName = argParts[0][0:parenOpenIndex]
            argType = argParts[0][parenOpenIndex+1:parenCloseIndex]
            argDesc = argParts[1].strip()

            addToDict(methodObj['arguments'],argumentType,{'argName':argName,'argType':argType,'argDesc':argDesc})
        

        #return
        returnTitle = filter(returnsFilter,args.select('dt'))
        if len(returnTitle) > 0:
            returnsObject = {}
            returnTitle = returnTitle[0]
            returnsObject['title'] = returnTitle.string
            returnDesc = filter(nextSiblingsFilter,returnTitle.next_siblings)
            returnsObject['desc'] = returnDesc[0].string
            methodObj['returns'] = returnsObject

        # add method
        addToDict(classDoc,methodTypeStr,methodObj)

    return classDoc

def createDocFile(classDoc,outputFile):

    htmlTemplate = '<div class="content"></div>'

    htmlDoc = BeautifulSoup(htmlTemplate,"html.parser")

    content = htmlDoc.select("div.content")[0]

    # title and class desc
    content.append(BeautifulSoup('<h2>{0}</h2>'.format(classDoc['title']),"html.parser"))
    content.append(BeautifulSoup('<p>{0}</p>'.format(classDoc['desc']),"html.parser"))
    content.append(createSOUPforMethod(classDoc['(Constructor)'][0],"Contructor",True))

    if 'Class Method' in classDoc:
        content.append(BeautifulSoup('<h2>{0}</h2>'.format('Class Methods'),'html.parser'))
        for classMethod in classDoc['Class Method']:
            content.append(createSOUPforMethod(classMethod,"Class Method"))
            
    content.append(BeautifulSoup('<h2>{0}</h2>'.format('Methods'),'html.parser'))

    for method in classDoc['method']:
        content.append(createSOUPforMethod(method,"Method"))


    #write to file
    outputFile = open(outputFile,'w')
    outputFile.write(htmlDoc.prettify())
    outputFile.close()
        

def createMethodMenuItem(methodName,methodType,docFile):
    return BeautifulSoup('<li><a href="{0}#{1}"><span class="type">{2}</span>{3}</a></li>'.format(docFile,
                                                                                                  methodName,
                                                                                                  methodType,
                                                                                                  methodName),
                         'html.parser')
			  
    

docFiles = [{'filename':'docs/discotech.provider.Provider-class.html',
             'outputFile':'api_docs/discotech.Provider.generated.html',
             'className': 'discotech.Provider',
             'docFile': '/discotech/docs/discotech.provider.base.html'},
            {'filename':'docs/discotech.providerSearcher.ProviderSearcher-class.html',
             'outputFile':'api_docs/discotech.ProviderSearcher.generated.html',
             'className': 'discotech.ProviderSearcher',
             'docFile': '/discotech/docs/discotech.ProviderSearcher.base.html'}]


#create menu

menuSOUP = BeautifulSoup('<ul></ul>','html.parser')

for docFile in docFiles:
    classDoc = docForFile(docFile['filename'],docFile['className'])
    createDocFile(classDoc,docFile['outputFile'])

    #class menu item
    menuItem = BeautifulSoup('<li></li>','html.parser')
    menuItem.li.append(BeautifulSoup('<a href="{0}">{1}</a>'.format(docFile['docFile'],docFile['className']),'html.parser'))

    #add methods

    methodsSOUP = BeautifulSoup('<ul></ul>','html.parser')
    
    #class methods
    if 'Class Method' in classDoc:
        for classMethod in classDoc['Class Method']:
            methodsSOUP.ul.append(createMethodMenuItem(classMethod['name'],'Class Method',docFile['docFile']))
    #methods
    for method in classDoc['method']:
            methodsSOUP.ul.append(createMethodMenuItem(method['name'],'Method',docFile['docFile']))


    menuItem.li.append(methodsSOUP)
    menuSOUP.ul.append(menuItem)


#save menu


menuFile = open('api_docs/menu.inc.generated.html','w')
menuFile.write(menuSOUP.prettify())
menuFile.close()

    


