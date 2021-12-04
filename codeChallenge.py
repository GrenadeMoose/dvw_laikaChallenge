import os
import shotgun_api3

html_out_dir = os.path.join(
    os.path.dirname(__file__),
    "html"
)


def shotgun_challenge(id, sequence_fields, shot_fields):
    """
    Initializes the connection to the shotgun server.
    Pulls requested information.
    Exports info to an HTML table
    """

    shotgun_api3.shotgun.NO_SSL_VALIDATION = True
    sg = shotgun_api3.Shotgun("https://laika-demo.shotgunstudio.com",
                              script_name="code_challenge",
                              api_key="$zvMznkhddo0tgwgwbftzaqob")
    # Be sure to close connection when you are done.
    sg.connect()

    filters = [
        ['project', 'is', {'type': 'Project', 'id': id}]
    ]

    shots = sg.find("Shot", filters, shot_fields)
    sequences = sg.find("Sequence", filters, sequence_fields)
    
    for s in shots:
        print(sg.schema_field_read("Shot", field_name="sg_latest_version", project_entity=s))

    sg.close()


if __name__ == "__main__":
    shotgun_challenge(id=85,
                      sequence_fields=["sg_cut_duration",
                                       "sg_ip_versions"],
                      shot_fields=["sg_latest_version"])
