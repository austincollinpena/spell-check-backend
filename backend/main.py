from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware import Middleware
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtension

# Local Packages
from backend.db import db as gino_db
from backend.utils.redis_client.seed_redis import seed_redis_site_blacklist, seed_redis

# For debugging:
import uvicorn

# Type defs
from backend.users.queries import user_query_schema
from backend.utils.graphql.query_type import query as root_query
from backend.utils.graphql.mutation_type import mutation as root_mutation
from backend.utils.graphql.subscription_type import subscription as root_subscription
from backend.utils.graphql import root_graphql_types
from backend.users import user_type_defs
from backend.scraper import scraper_type_defs

schema = make_executable_schema(
    [*root_graphql_types, *user_type_defs, *scraper_type_defs], root_query, root_mutation, root_subscription)

from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware


class BackgroundTaskMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.background = None
        response = await call_next(request)
        if request.state.background:
            response.background = request.state.background
        return response


middleware = [
    Middleware(BackgroundTaskMiddleware),
    Middleware(CORSMiddleware, allow_origins=['http://localhost:3000'], allow_methods=['*'], allow_headers=["*"],
               allow_credentials=[True])
]

app = Starlette(debug=True, middleware=middleware, on_startup=[seed_redis_site_blacklist, seed_redis])
gino_db.init_app(app)

# load_modules(app)
app.mount("/graphql", GraphQL(schema, debug=True,
                              extensions=[ApolloTracingExtension]))

# For debugging
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8002)

# TODO: When running celery from docker don't do it in a dumb way
# TODO: https://www.uvicorn.org/settings/ - deploy correctly


# uvicorn backend.main:app --reload --port 8002
