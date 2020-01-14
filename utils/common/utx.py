#!/usr/bin/env python
# coding=utf-8

import functools
import unittest
from time import sleep
from enum import Enum, unique
from utils.common.log import logger
from utils.config import Config

CASE_ID_FLAG = "__case_id__"
CASE_INFO_FLAG = "__case_info__"
CASE_TAG_FLAG = "__case_tag__"


def _handler(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        sleep(0.5)
        msg = "start to test {} ({}/{})".format(getattr(func, CASE_INFO_FLAG),
                                                getattr(func, CASE_ID_FLAG),
                                                Tool.total_case_num)
        logger.info(msg)
        result = func(*args, **kwargs)
        return result

    return wrap


@unique
class Tag(Enum):
    SMOKE = 1000  # Don't Delete or change
    ALL = 1  # Don't Delete or change

    # level:
    HIGH = 200
    MEDIUM = 20
    LOW = 2


def tag(*tag_type):
    """
    support Multiple tags
    @tag(Tag.SMOKE, Tag.MEDIUM)
    def test_func(self):
        pass
    :param tag_type: define at class Tag
    :return:
    """

    def wrap(func):
        if not hasattr(func, CASE_TAG_FLAG):
            tags = set()
            tags.update(tag_type)
            setattr(func, CASE_TAG_FLAG, tags)
        else:
            getattr(func, CASE_TAG_FLAG).update(tag_type)
        return func

    return wrap


class Tool(object):
    total_case_num = 0

    @classmethod
    def general_case_id(cls):
        cls.total_case_num += 1
        return cls.total_case_num

    @staticmethod
    def filter_test_case(funcs_dict):
        funcs = dict()
        cases = dict()
        for i in funcs_dict:
            if i.startswith("test_"):
                cases[i] = funcs_dict[i]
            else:
                funcs[i] = funcs_dict[i]
        return funcs, cases.items()

    @staticmethod
    def modify_raw_func_name(raw_func_name, raw_func):
        case_id = Tool.general_case_id()
        setattr(raw_func, CASE_ID_FLAG, case_id)
        func_name = raw_func_name.replace("test_", "test_{:05d}_".format(case_id))

        return func_name

    @staticmethod
    def recreate_case(raw_func_name, raw_func):
        result = dict()
        func_name = Tool.modify_raw_func_name(raw_func_name, raw_func)
        if len(func_name) > 80:
            func_name = func_name[:80] + "……"
        result[func_name] = _handler(raw_func)
        return result


run_tag = Tag[Config().get("AeMS").get("run_case")]


def is_case_run(tags_list):
    is_run = False
    for a_tag in tags_list:
        if a_tag.value > run_tag.value:
            is_run = True  # 只执行value 更大的
            break
    return is_run


class Meta(type):
    def __new__(mcs, class_name, bases, func_names):
        """
        :param class_name: 类名
        :param bases: 父类, 继承自,
        :param func_names: 方法名
        """
        funcs, cases = Tool.filter_test_case(func_names)
        for raw_case_name, raw_case in cases:
            # 注入用例信息
            case_info = "{}.{}".format(raw_case.__module__, raw_case.__name__)
            setattr(raw_case, CASE_INFO_FLAG, case_info)

            # 如果没有tag, 则默认注入Tag.All
            if not hasattr(raw_case, CASE_TAG_FLAG):
                tags = {Tag.ALL}
                setattr(raw_case, CASE_TAG_FLAG, tags)

            tags_list = list(getattr(raw_case, CASE_TAG_FLAG))
            if not is_case_run(tags_list):
                continue

            # funcs.update(Tool.recreate_case(raw_case_name, raw_case))
            # func_names = funcs
        return super(Meta, mcs).__new__(mcs, class_name, bases, func_names)


class _TestCase(unittest.TestCase, metaclass=Meta):
    def shortDescription(self):
        doc = self._testMethodDoc
        doc = doc and doc.split()[0].strip() or None
        return doc


TestCase = _TestCase
