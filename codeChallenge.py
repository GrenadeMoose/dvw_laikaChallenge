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

    # Do the query
    for entity, fields in queries.items():
        for field in fields:
            field_config = sg.schema_field_read(entity, field)
            print(field_config)
            sg.find(entity, field_config[field]['properties']['query']['value']['filters'], [field])
        res = sg.find(entity, filters, fields, filter_operator='any')
        save_to_html(res, entity, fields)

    # Closing connection
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
        table.append("\t\t<td>{0}</td>".format(r['type']))
        table.append("\t\t<td>{0}</td>".format(r['id']))
        for field in fields:
            if field in r.keys():
                table.append("\t\t<td>{0}</td>".format(r[field]))
            else:
                table.append("\t\t<td>FIELD ERROR</td>")
        table.append("\t</tr>")

    table.append("</table>")

    # Create directory if none exists
    if not os.path.exists(html_out_dir):
        os.mkdir(html_out_dir)

    # Write output to html
    with open(os.path.join(html_out_dir, "{}.html".format(entity)), 'w') as outfile:
        outfile.write('\n'.join(table))


if __name__ == "__main__":
    shotgun_challenge(85,
                      {"Sequence": ["sg_cut_duration",
                                    "sg_ip_versions"],
                       "Shot": ["sg_latest_version"]
                       })
