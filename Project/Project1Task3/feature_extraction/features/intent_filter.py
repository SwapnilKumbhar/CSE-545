from lxml.etree import _Element

NON_MALICIOUS_INTENTS = [
    "android.intent.action.MAIN",
    "android.intent.action.VIEW"
]

ANDROID_NAME = "{http://schemas.android.com/apk/res/android}name"

def get_malicious_intents(intent_filters):
    malicious_intent_filters = 0
    for intent in intent_filters:
        if intent.tag == "action" and ANDROID_NAME in intent.attrib.keys() and intent.attrib[ANDROID_NAME] not in NON_MALICIOUS_INTENTS:
            malicious_intent_filters += 1
            print(intent.attrib[ANDROID_NAME])
    return malicious_intent_filters

def get_features(manifest: _Element, feature_vector):
    if manifest is None:
        feature_vector.append(-1)
        return

    activity_elems = manifest.findall("activity")

    intent_filters = 0

    for activity in activity_elems:
        for child in activity:
            if child.tag == "intent-filter":
                malicious_intent_filters = get_malicious_intents(child)
                if malicious_intent_filters > 0:
                    intent_filters += 1

    feature_vector.append(intent_filters)
