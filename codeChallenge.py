import os
import shotgun_api3

html_out_dir = os.path.join(
    os.path.dirname(__file__),
    "html"
)


def shotgunChallenge(id, sequenceFields, shotFields):
    """
    Initializes the connection to the shotgun server.
    Pulls requested information.
    Exports info to an HTML table
    """

    shotgun_api3.shotgun.NO_SSL_VALIDATION = True
    sg = shotgun_api3.Shotgun("https://laika-demo.shotgunstudio.com",
                              login="code_challenge",
                              password="$zvMznkhddo0tgwgwbftzaqob")
    # Be sure to close connection when you are done.
    sg.connect()

    # Do the stuff

    sg.close()


if __name__ == "__main__":
    shotgunChallenge(id="85",
                     sequenceFields=["sg_cut_duration",
                                     "sg_ip_versions"],
                     shotFields=["sg_latest_version"])
