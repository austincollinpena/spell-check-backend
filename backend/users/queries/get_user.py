from backend.utils.graphql.query_type import query
from starlette.authentication import requires
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse


@query.field("getUser")
async def resolve_get_user(obj, info):
    tasks = BackgroundTasks()
    tasks.add_task(testFunc)
    return False


async def testFunc():
    print('I did it!')
