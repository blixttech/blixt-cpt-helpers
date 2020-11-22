from cpt.packager import ConanMultiPackager
from cpt.ci_manager import CIManager
from conans.client import conan_api
from cpt.printer import Printer
import os
import sys
import re
import traceback
import configparser


def hidesensitive(output):
    output_str = str(output)
    output_str = re.sub(r'(CONAN_LOGIN_USERNAME[_\w+]*)=\"(\w+)\"', r'\1="xxxxxxxx"', output_str)
    output_str = re.sub(r'(CONAN_PASSWORD[_\w+]*)=\"(\w+)\"', r'\1="xxxxxxxx"', output_str)
    sys.stdout.write(output_str)


def get_recipe_path(cwd=None):
    conanfile = os.getenv("CONAN_CONANFILE", "conanfile.py")
    if cwd is None:
        return os.path.abspath(conanfile)
    else:
        return os.path.join(cwd, conanfile)


def get_bool_from_env(var_name, default="1"):
    val = os.getenv(var_name, default)
    return str(val).lower() in ("1", "true", "yes", "y")


def get_value_from_recipe(search_string, recipe=None):
    if recipe is None:
        recipe = get_recipe_path()
    with open(recipe, "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result


def inspect_value_from_recipe(attribute, recipe_path):
    try:
        conan_instance, _, _ = conan_api.Conan.factory()
        inspect_result = conan_instance.inspect(path=recipe_path, attributes=[attribute])
        return inspect_result.get(attribute)
    except:
        pass
    return None


def get_name_from_recipe(recipe=None):
    name = inspect_value_from_recipe(attribute="name", recipe_path=get_recipe_path())
    if name:
        return name
    else:
        result = get_value_from_recipe(r'''name\s*=\s*["'](\S*)["']''', recipe=recipe)
        if result:
            return result.groups()[0]
        else:
            return None


def get_version_from_recipe(recipe=None):
    version = inspect_value_from_recipe(attribute="version", recipe_path=get_recipe_path())
    if version:
        return version
    else:
        result = get_value_from_recipe(r'''version\s*=\s*["'](\S*)["']''', recipe=recipe)
        if result:
            return result.groups()[0]
        else:
            return None


def get_version_from_ci():
    printer = Printer(hidesensitive)
    ci_man = CIManager(printer)
    return re.sub(".*/", "", ci_man.get_branch())


def get_name_and_version():
    return get_name_from_recipe(), get_version_from_recipe() or get_version_from_ci()
