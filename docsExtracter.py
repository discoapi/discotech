from pprint import pprint
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("docs/discotech.provider.Provider-class.html"))


htmlTemplate = '<div class="content"></div>'

classDoc = {}

def createSOUPforMethod(methodObj):
    htmlStart = "<h3>{0}</h3><p>{1}</p>".format(methodObj.signature,methodObj.desc)

    

def addToDict(dictObj,name,obj):
    if name in dictObj:
        dictObj[name].append(obj)
    else:
        dictObj[name] = [obj]

def has_sig(tag):
    return tag.select('spag.sig') != None


def codeFilter(outputList):
    def filterFunc(item):
        if item in outputList:
            return False
        if item == '>>> ':
            return False
        return True
    return filterFunc
    
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

        addToDict(methodObj,argumentType,{'argName':argName,'argType':argType,'argDesc':argDesc})
        
        #print "argName:{0} argType:{1} argDesc:{2}".format(argName,argType,argDesc)
    addToDict(classDoc,methodTypeStr,methodObj)

#pprint(classDoc)

htmlDoc = BeautifulSoup(htmlTemplate)

content = htmlDoc.select("div.content")[0]



print(htmlDoc.prettify())



        
    
