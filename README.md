### LNDB.INFO API (Made by pro-beginner)
This is a simple API I modified to get data from [LNDB.info - The Light Novel Database](lndb.info)

Sample of API : [Demo](https://lndb-api.herokuapp.com/docs)

There are two method in this api:
1. Light Novel Search: Enter any keyword and it will return array of title and lndb-links of search result.
2. Light Novel Detail: This is a bit confusing. You take the lndb-link, remove HTTP://LNDB.INFO/LIGHT_NOVEL/ part and enter the remaining part. It will return a json of { Title, Author, Illustrator, Plot, Genre as List, Volumes, Alternative Titles as List, Covers as list of image address.

Please add your domain as origin before use.

#####This project is a modified clone of https://github.com/riojano0/lndb-info-api/
