# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 11:17:44 2016

@author: Nic.Austin
"""
# pylint: disable=C0103
# pylint: disable=E1101

from lxml.builder import ElementMaker
from lxml import etree

# Set up useful builders and namespaces
__base = "http://www.grantadesign.com/16/01/"
ns = {'soapenv': "http://schemas.xmlsoap.org/soap/envelope/",
      'xsi': "http://www.w3.org/2001/XMLSchema-instance",
      'base': __base,
      'ser': __base + "Search",
      'gbt': __base + "GrantaBaseTypes",
      'exp': __base + "DataExport",
      'rep': __base + "Reporting",
      'grt': __base + "GrantaReportTypes",
      'eng': __base + "EngineeringData",
      'inp': __base + "DataImport",
      'brw': __base + "Browse",
      'hdr': 'http://www.grantadesign.com/headers'}

ENV = ElementMaker(namespace=ns['soapenv'], nsmap=ns)
SER = ElementMaker(namespace=ns['ser'], nsmap=ns)
GBT = ElementMaker(namespace=ns['gbt'], nsmap=ns)
EXP = ElementMaker(namespace=ns['exp'], nsmap=ns)
REP = ElementMaker(namespace=ns['rep'], nsmap=ns)
GRT = ElementMaker(namespace=ns['grt'], nsmap=ns)
ENG = ElementMaker(namespace=ns['eng'], nsmap=ns)
INP = ElementMaker(namespace=ns['inp'], nsmap=ns)
BRW = ElementMaker(namespace=ns['brw'], nsmap=ns)
HDR = ElementMaker(namespace=ns['hdr'], nsmap=ns)

parser = etree.XMLParser(ns_clean=True, recover=True)

def partialTableRef(tableName):
    """Create a partial table refeference based on table name"""

    return GBT.table(GBT.tableName(tableName))

def attrRef(dbKey, tableName, attributeName, *args):
    """Create an attribute refernce based on attribute name"""

    ref = GBT.attribute(GBT.dbKey(dbKey), GBT.name(partialTableRef(tableName), GBT.attributeName(attributeName)))
    ref.set("{%s}type" % ns['xsi'], "gbt:MIAttributeReference")
    if args:
        return updateTag(ref, args[0])

    return ref

def subsetRef(dbKey, tableName, subsetName):
    """Create a subset reference based on subset name"""

    return GBT.subset(GBT.dbKey(dbKey), GBT.name(partialTableRef(tableName), GBT.subsetName(subsetName)))

def recordLinkGroupRef(dbKey, tableName, linkGroupName, *args):
    """Create a record link group reference based on record link group name"""

    ref = GBT.recordLinkGroup(GBT.dbKey(dbKey), GBT.name(partialTableRef(tableName), GBT.recordLinkGroupName(linkGroupName)))
    if args:
        return updateTag(ref, args[0])

    return ref

def recordRef(dbKey, tableName, fullName, *args):
    """Create a record reference based on record name"""

    aRef = GBT.attributeReference(GBT.name(partialTableRef(tableName), GBT.pseudo("name")))
    ref = GBT.record(GBT.dbKey(dbKey), GBT.lookupValue(aRef, GBT.attributeValue(fullName)))
    if args:
        return updateTag(ref, args[0])

    return ref

def updateTag(element, tag):
    """Mutate the tag name of an element"""

    p, e = tag.split(":")
    element.tag = "{%s}%s" % (ns[p], e)

    return element

def printXML(xml):
    """Pretty print an etree element"""

    print etree.tostring(xml, pretty_print=True)

def exportRecordData(s, host, dbKey, tableName, recordRef, attrNames):
    """Export multiple attributes for a single record"""

    aRefs = [attrRef(dbKey, tableName, a, 'exp:result') for a in attrNames]
    exp = EXP.GetRecordAttributesByRef(*aRefs)
    exp.append(updateTag(recordRef, "exp:recordReference"))

    body = ENV.Envelope(ENV.Body(exp))
    headers = {'SOAPAction': ns["exp"] + "/GetRecordAttributesByRefRequest"}
    response = s.post(host+'DataExport.svc', data=etree.tostring(body), headers=headers)
    tree = etree.fromstring(response.content, parser)

    attrValues = {}
    find = etree.XPath("descendant::gbt:attributeValues/gbt:attributeValue", namespaces=ns)
    for attrValue in find(tree):
        attrName = attrValue.xpath("gbt:AttributeName", namespaces=ns)[0].text
        attrValues[attrName] = attrValue

    return attrValues

def recordNameSearch(s, host, dbKey, table, name):
    """Locate a record by name"""

    ser = SER.RecordNameSearch()
    t = SER.table(GBT.tableName(table), GBT.dbKey(dbKey))
    ser.append(t)
    ser.append(SER.recordName(name))

    body = ENV.Envelope(ENV.Body(ser))
    headers = {'SOAPAction': ns["ser"] + "/RecordNameSearchRequest"}
    response = s.post(host+'Search.svc', data=etree.tostring(body), headers=headers)
    tree = etree.fromstring(response.content, parser)

    recordRef = tree.xpath("descendant::gbt:recordReference", namespaces=ns)[0]

    return recordRef

def ensureFolderPath(s, host, dbKey, tableName, folderPath):
    """Ensure that a folder path exists before creating a new record"""

    # Locate the root node of the table
    brw = BRW.GetRootNode(BRW.table(GBT.tableName(tableName), GBT.dbKey(dbKey)))

    body = ENV.Envelope(ENV.Header(), ENV.Body(brw))
    headers = {'SOAPAction': ns["brw"] + "/GetRootNodeRequest"}
    response = s.post(host+'Browse.svc', data=etree.tostring(body), headers=headers)
    tree = etree.fromstring(response.content, parser)

    rootNode = tree.xpath("descendant::gbt:recordReference", namespaces=ns)[0]

    # Now ensure the folder path,returning the leaf node
    treeNames = INP.treeNames(*[INP.treeName(f) for f in folderPath.split("/")])
    rootNode = updateTag(rootNode, "inp:parent")
    path = INP.folderPaths(INP.folderPath(rootNode, treeNames))
    inp = INP.EnsureRecordFolderPathsRequest(path)

    body = ENV.Envelope(ENV.Header(), ENV.Body(inp))
    headers = {'SOAPAction': ns["inp"] + "/EnsureRecordFolderPathsRequest"}
    response = s.post(host+'DataImport.svc', data=etree.tostring(body), headers=headers)
    tree = etree.fromstring(response.content, parser)

    leaf = tree.xpath("descendant::gbt:recordReference", namespaces=ns)[0]

    return leaf

def storeResults(s, host, dbKey, tableName, folderPath, subset, recordName, data):
    """Create a new record and populate it with simple data"""

    # Ensure that the record folder path exists
    folder = ensureFolderPath(s, host, dbKey, tableName, folderPath)
    updateTag(folder, "gbt:parentRecord")

    attrs = []
    values = []
    for a, v in data.items():
        attrs.append(a)
        values.append(v)

    attrTypes = MITypes(s, host, dbKey, tableName, attrs)

    # Add these MIValue to the set of data to import
    iav = GBT.importAttributeValues()
    for attr, value in zip(attrs, values):
        iv = GBT.importAttributeValue(attrRef(dbKey, tableName, attr), MIValue(attrTypes[attr], value))
        iav.append(iv)

    # Now create a new result record in MI
    inp = INP.SetRecordAttributesRequest(INP.importRecords(GBT.create(
        iav,
        GBT.recordName(recordName),
        GBT.subsetReferences(subsetRef(dbKey, tableName, subset)),
        folder)))

    body = ENV.Envelope(ENV.Body(inp))
    headers = {'SOAPAction': ns["inp"] + "/SetRecordAttributesRequest"}
    response = s.post(host+'DataImport.svc', data=etree.tostring(body), headers=headers)

def MIValue(MIType, value):
    """Return an appropriate representation of a dataum given a datum's type and value"""

    if MIType == 'POIN':
        point = GBT.Point(GBT.Value(str(value)), GBT.ValueParameters())
        return GBT.value(GBT.PointDataValue(GBT.Parameters(), point))
    elif MIType == 'DTTM':
        return GBT.value(GBT.DateDataValue(value))

def MITypes(s, host, dbKey, tableName, attributeNames):
    """Return attributes types for a set of attributes"""

    aRefs = [attrRef(dbKey, tableName, a) for a in attributeNames]
    brw = BRW.GetAttributeDetails(GBT.attributeReferences(*aRefs))

    body = ENV.Envelope(ENV.Header(), ENV.Body(brw))
    headers = {'SOAPAction': ns["brw"] + "/GetAttributeDetailsRequest"}
    response = s.post(host+'Browse.svc', data=etree.tostring(body), headers=headers)
    tree = etree.fromstring(response.content, parser)

    types = {}
    for a in tree.xpath("descendant::gbt:attributeDetail", namespaces=ns):
        attrName = a.xpath("gbt:name", namespaces=ns)[0].text
        attrType = a.xpath("gbt:type", namespaces=ns)[0].text
        types[attrName] = attrType

    return types
