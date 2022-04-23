"id": "1",
"jobnumber": "keksieskdo",
"description": "dkdieksdoies",
"customer": "keksieskdo",
"user_id": "1",
"date_create": "2022-01-02 08:08:34.750696",
"date_due": " ",
"date_modify": " ",
"date_finish": " ",

"(?<oo>[a-zA-Z0-9_]+)": "(?<foo>[a-zA-Z0-9- :.]+)",
$1=StringField( $2 )



id=StringField( )
jobnumber=StringField( )
description=StringField( )
customer=StringField( )
user_id=StringField( )
date_create=StringField( )
date_due=StringField( )
date_modify=StringField( )
date_finish=StringField( )




(?<foo>"[.a-zA-Z0-9_-]+"):(?<o>"[,+-.a-zA-Z0-9_ ]+"),
$1['$2']


show dbs
use TinyMRP

db.part.deleteMany({  partnumber: RegExp('TMRP')})





allparts=mongoPart.objects()
paco=allparts(partnumber="AWS-A-010174")[0]
paco.updateFileset()
pepo=mongoFileSet(description="test")

allparts=mongoPart.objects()
for part in allparts: part.updateFileset()


allparts=mongoPart.objects()

for part in allparts:
    part.fileset=None
    part.save()


allparts=mongoPart.objects()
paco=allparts(partnumber="200366-GA")[0]
test=paco.treeDict()
test['children']


paco.get_components()



import pymongo
import csv

client = pymongo.MongoClient("localhost", 27017)
db=client.TinyMRP
partcol=db["part"]

for part in partcol.find():
    partcol.update_one({"_id":part["_id"]},{"$unset":{"id":""}})




allparts=mongoPart.objects()
paco=allparts(partnumber="AWS-A-010174")[0]

parents=paco.getparents()
children=paco.getchildren()


pepe=allparts(partnumber="AWS-A-010176")[0]


paco.hasProcess("purchase")
paco.hasProcess("machine")
paco.hasConsumingProcess()



testpart=allparts[1]
testpart.getparents()



test=partcol.find_one({'partnumber':"OEM-TNM10W"})
parents=partcol.find({'children':{ '$elemMatch' :{'pk':test.pk}}})


test=mongoPart().objects(partnumber="OEM-TNM10W")




test=partcol.find({'pk':{'$in:'}})




allparts(description__icontains="bean")


allparts=allparts(Q(description__icontains="bean") & Q( description__icontains="pro"))




pipeline = [ {"$match": {}}, 
             {"$out": "part"},
]
mongodb.destination_collection.aggregate(pipeline)


sudo kill -9 $(sudo lsof -t -i:5000)




allparts=mongoPart.objects()
i=1
for part in allparts:
    if i<4500: 
        i=i+1
        part.delete()
        part.save()



allparts=mongoPart.objects()
i=1
for part in allparts:
        part.delete()
        part.save()












