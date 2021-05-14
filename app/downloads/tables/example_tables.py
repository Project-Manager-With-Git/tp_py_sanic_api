import datetime
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic_openapi import doc


@doc.summary("获取示例表格")
@doc.tag("downloads")
@doc.tag("tables")
@doc.description("获取某日的示例表格")
async def example_tables(request: Request, date: datetime.date) -> HTTPResponse:
    date_str = date.strftime("%Y-%m-%d")
    response = await request.respond(content_type="text/csv", headers={"Content-Disposition": f"attachment;filename={date_str}.csv"})
    await response.send("foo,bar\r\n")
    await response.send("a,1\r\n")
    await response.send("b,2\r\n")
    await response.send("c,3\r\n", True)
    return response
