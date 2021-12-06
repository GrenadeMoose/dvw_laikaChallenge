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
            # Attempt to clean up filter and query to read the Query Field data via API
            # According to the documentation, this is not supported. But it sounds like
            # this can be done by reworking the format of a schema field to fit into a
            # find or summarize call.
            field_config = sg.schema_field_read(entity, field)

            query_entity = field_config[field]['properties']['query']['value']['entity_type']
            query_filters = field_config[field]['properties']['query']['value']['filters']
            query_field = field_config[field]['properties']['summary_field']

            # Prep the query filters
            prep_query(query_filters, entity)
            query_filters['conditions'].append(filters[0])

            # This does not work yet.
            #item = sg.find(entity, query_filters, [field])

        res = sg.find(entity, filters, fields, filter_operator='any')
        save_to_html(res, entity, fields)

    # Closing connection
    sg.close()


def prep_query(query, entity):
    """
    This is an attempt to get a query field's filter to be readable by a find or summarize call
    :param query: The query filters pulled from a schema_field_read
    :param entity: The entity that relates to the query field
    :return: reformatted query with active removed, and parent_entity_token pointed toward the correct entity type
    """
    if (isinstance(query, dict)):
        for k in list(query):
            prep_query(query[k], entity)
            if 'active' == k:
                del query[k]
    elif isinstance(query, list):
        for i in reversed(range(len(query))):
            if isinstance(query[i], dict):
                if 'active' in query[i] and query[i]['active'] == 'false':
                    del query[i]
                if 'parent_entity_token' in query[i].values():
                    query[i] = entity
                prep_query(query[i], entity)


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
