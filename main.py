from db.sqlalchemy_database import db
import asyncio
from datetime import datetime

async def main(): 
    # await db.add_publication("UUUU", "sdkjfkjsadhgf", "skdfaskdflasf", datetime.today(), "sdfksldfj")
    for i in await db.get_publications():
        print(i.title)

    await db.update_publication('c1075446-f19d-4613-96a4-47c4d5eb52a6', 'Aboba', 'aa', '', datetime.today(), '234')
    print()

    for i in await db.get_publications():
        print(i.title)


asyncio.run(main())