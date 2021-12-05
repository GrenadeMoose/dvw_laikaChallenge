import os
import shotgun_api3

html_out_dir = os.path.join(
    os.path.dirname(__file__),
    "html"
)

server_path = "https://laika-demo.shotgunstudio.com"
script_name = "code_challenge"
api_key = "$zvMznkhddo0tgwgwbftzaqob"


def shotgun_challenge(id, queries):
    """
    Initializes the connection to the shotgun server.
    Queries requested information.
    Calls save_to_html to handle exporting query to html table.

    :param id: Sequence id to be queried
    :param queries: a dict of entity type strings and field lists to be queried
    """

    shotgun_api3.shotgun.NO_SSL_VALIDATION = True
    sg = shotgun_api3.Shotgun(server_path,
                              script_name=script_name,
                              api_key=api_key)
    # Be sure to close connection when you are done.
    sg.connect()

    filters = [
        ['project', 'is', {'type': 'Project', 'id': id}]
    ]

    for entity, fields in queries.items():
        res = sg.find(entity, [['project.Project.id', 'is', id]], fields)
        save_to_html(res, entity, fields)

    sg.close()


def save_to_html(query_results, entity, fields):
    """
    Saving the query results to an HTML file.

    :param query_results: The results of the shotgun_challenge query as a list of dicts
    :param entity: String identifier for the entity
    :param fields: String list of fields queried in shotgun_challenge

    :output: html table of query results saved to html_out_dir
    """
    table = ["<table>", "\t<tr>"]

    # Append headers
    table.append("\t\t<th>Type</th>")
    table.append("\t\t<th>ID</th>")
    for field in fields:
        table.append("\t\t<th>{0}</th>".format(field))
    table.append("\t</tr>")

    # Append values
    for r in query_results:
        table.append("\t\t<th>{0}</th>".format(r['type']))
        table.append("\t\t<th>{0}</th>".format(r['id']))
        for field in fields:
            table.append("\t\t<th>{0}</th>".format(r[field]))
        table.append("\t</tr>")

    table.append("</table>")

    if not os.path.exists(html_out_dir):
        os.mkdir(html_out_dir)

    with open(os.path.join(html_out_dir, "{}.html".format(entity)), 'w') as outfile:
        outfile.write('\n'.join(table))


if __name__ == "__main__":
    shotgun_challenge(85,
                      {"Sequence": ["sg_cut_duration",
                                    "sg_ip_versions"],
                       "Shot": ["sg_latest_version"]
                       })
