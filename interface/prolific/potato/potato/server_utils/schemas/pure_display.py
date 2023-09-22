"""
Pure Display Layout
"""


def generate_pure_display_layout(annotation_scheme):

    if annotation_scheme["description"] != "":
        desc = """<div class="card-body">
                          <p class="card-text"> {:}</p>
                          </div>""".format(annotation_scheme["description"])
    else:
        desc = ""
    schematic = """<div class="col-md-12 my-4">
                    <div class="card">
                        <h5 class="card-header">%s</h5>
                         %s
                        </div>
                    </div>""" % (
        annotation_scheme["name"],
        desc
    )

    return schematic, []
