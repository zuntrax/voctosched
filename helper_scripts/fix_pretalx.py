#!/usr/bin/python3
"""
pretalx generates different slugs which are not suitable for media.ccc.de
also emojis seem to be allowed in room names, they need to be replaced
"""
from xml.etree import ElementTree
from emoji import demojize
from io import StringIO

from fahrplan.slug import StandardSlugGenerator
from fahrplan.uuid import uuid
from util import read_file


def fix_room_name(name: str):
    name = demojize(name)
    name = StandardSlugGenerator.normalize_name(name)
    return name


def fix_tree(tree: ElementTree, acronym: str = None):
    root = tree.getroot()
    if acronym is None:
        acronym = tree.find("conference").find("acronym").text
    else:
        tree.find("conference").find("acronym").text = acronym
    slug = StandardSlugGenerator(acronym)

    for room in root.iter('room'):
        try:
            name = room.attrib['name']
            room.attrib['name'] = fix_room_name(name)
        except KeyError:
            continue

    for event in root.iter('event'):
        event_room = event.find('room').text
        event.find('room').text = fix_room_name(event_room)

        event_id = event.attrib['id']
        event_title = event.find('title').text
        event_slug = slug.generate(event_id, event_title)
        event.find('slug').text = event_slug

        event.attrib['guid'] = uuid(event_id, event_title)

    return tree


def main():
    orig = 'https://2018.djangocontent.eu/hd/schedule/export?exporter=core-frab-xml'
    output = '/tmp/fahrplan-django.xml'
    acronym = "djangocon_eu_2018"

    content = read_file(orig)
    with StringIO(content) as schedule:
        tree = ElementTree.parse(schedule)
    tree = fix_tree(tree, acronym)
    tree.write(output)
    print('schedule written to ' + output)


if __name__ == "__main__":
    main()
