"""
Multiselect Layout
"""

import logging
from collections.abc import Mapping

logger = logging.getLogger(__name__)


def generate_multiselect_layout(annotation_scheme):
    schematic = (
        '<form action="/action_page.php">'
        + "  <fieldset>"
        + ("  <legend>%s</legend>" % annotation_scheme["description"])
    )

    # TODO: display keyboard shortcuts on the annotation page
    key2label = {}
    label2key = {}

    key_bindings = []

    display_info = (
        annotation_scheme["display_config"] if "display_config" in annotation_scheme else {}
    )

    n_columns = display_info["num_columns"] if "num_columns" in display_info else 1

    schematic += "<table>"

    # setting up label validation for each label, if "required" is True, the annotators will be asked to finish the current instance to proceed
    validation = ""
    label_requirement = (
        annotation_scheme["label_requirement"] if "label_requirement" in annotation_scheme else None
    )
    if label_requirement and label_requirement["required"]:
        validation = "required"

    # if right_label is provided, the associated label has to be clicked to proceed. This is normally used for consent questions at the beginning of a survey.
    right_label = set()
    if label_requirement and "right_label" in label_requirement:
        if type(label_requirement["right_label"]) == str:
            right_label.add(label_requirement["right_label"])
        elif type(label_requirement["right_label"]) == list:
            right_label = set(label_requirement["right_label"])
        else:
            logger.warning("Incorrect format of right_label %s" % label_requirement["right_label"])
            # quit()

    for i, label_data in enumerate(annotation_scheme["labels"], 1):

        if (i - 1) % n_columns == 0:
            schematic += "<tr>"
        schematic += "<td>"

        label = label_data if isinstance(label_data, str) else label_data["name"]

        name = annotation_scheme["name"] + ":::" + label
        class_name = annotation_scheme["name"]
        key_value = name

        tooltip = ""
        if isinstance(label_data, Mapping):
            tooltip_text = ""
            if "tooltip" in label_data:
                tooltip_text = label_data["tooltip"]
                # print('direct: ', tooltip_text)
            elif "tooltip_file" in label_data:
                with open(label_data["tooltip_file"], "rt") as f:
                    lines = f.readlines()
                tooltip_text = "".join(lines)
                # print('file: ', tooltip_text)
            if len(tooltip_text) > 0:
                tooltip = (
                    'data-toggle="tooltip" data-html="true" data-placement="top" title="%s"'
                    % tooltip_text
                )

            if "key_value" in label_data:
                key_value = label_data["key_value"]
                if key_value in key2label:
                    logger.warning("Keyboard input conflict: %s" % key_value)
                    quit()
                key2label[key_value] = label
                label2key[label] = key_value
                key_bindings.append((key_value, class_name + ": " + label))

        if (
            "sequential_key_binding" in annotation_scheme
            and annotation_scheme["sequential_key_binding"]
            and len(annotation_scheme["labels"]) <= 10
        ):
            key_value = str(i % 10)
            key2label[key_value] = label
            label2key[label] = key_value

        label_content = label
        if annotation_scheme.get("video_as_label", None) == "True":
            assert (
                "videopath" in label_data
            ), "Video path should in each label_data when video_as_label is True."
            video_path = label_data["videopath"]
            label_content = f"""
            <video width="320" height="240" autoplay loop muted>
                <source src="{video_path}" type="video/mp4" />
            </video>"""

        # add shortkey to the label so that the annotators will know how to use it
        # when the shortkey is "None", this will not displayed as we do not allow short key for None category
        # if label in label2key and label2key[label] != 'None':
        # if label in label2key:
        #    label_content = label_content + \
        #        ' [' + label2key[label].upper() + ']'

        final_validation = "right_label" if label in right_label else validation

        if ("single_select" in annotation_scheme) and (
            annotation_scheme["single_select"] == "True"
        ):
            logger.warning(
                'single_select is Depricated and will be removed soon. Use "radio" instead.'
            )
            schematic += (
                '  <input class="%s" type="checkbox" id="%s" name="%s" value="%s" onclick="onlyOne(this)" validation="%s">'
                + '  <label for="%s" %s>%s</label><br/>'
            ) % (class_name, name, name, key_value, final_validation, name, tooltip, label_content)
        else:
            schematic += (
                '<label for="%s" %s><input class="%s" type="checkbox" id="%s" name="%s" value="%s" onclick="whetherNone(this)" validation="%s">'
                + "  %s</label><br/>"
            ) % (name, tooltip, class_name, name, name, key_value, final_validation, label_content)

        schematic += "</td>"
        if i % n_columns == 0:
            schematic += "</tr>"

    if "has_free_response" in annotation_scheme and annotation_scheme["has_free_response"]:

        label = "free_response"
        name = annotation_scheme["name"] + ":::free_response"
        class_name = annotation_scheme["name"]
        tooltip = "Entire a label not listed here"
        instruction = (
            "Other"
            if "instruction" not in annotation_scheme["has_free_response"]
            else annotation_scheme["has_free_response"]["instruction"]
        )

        schematic += (
            '<tr><td colspan="%s"><div style="float:left; display:flex; flex-direction:row;">%s <input class="%s" type="text" id="%s" name="%s">'
            + '  <label for="%s" %s></label></div></td</tr>'
        ) % (str(n_columns), instruction, class_name, name, name, name, tooltip)

    schematic += "</table>"
    schematic += "  </fieldset>\n</form>\n"

    return schematic, key_bindings
