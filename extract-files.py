#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# Copyright (C) 2020 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sm8350',
    'vendor/xiaomi/mojin',
    'vendor/qcom/opensource/display',
]

blob_fixups: blob_fixups_user_type = {
    ('vendor/etc/camera/pureShot_parameter.xml', 'vendor/etc/camera/pureView_parameter.xml'): blob_fixup()
        .regex_replace(r'=([0-9]+)>', r'="\1">'),
    'vendor/etc/camera/mona_motiontuning.xml': blob_fixup()
        .regex_replace(r'xml=version="1\.0"', 'xml version="1.0"'),
    'vendor/lib64/hw/camera.qcom.so': blob_fixup()
        .binary_regex_replace(b'st_license\\.lic', b'camera_cnf.txt')
        .add_needed('libprocessgroup_shim.so'),
    'vendor/lib64/hw/camera.xiaomi.so': blob_fixup()
        .sig_replace(
            '21 00 80 52 29 07 00 94',
            '21 00 80 52 1F 20 03 D5',
        ),
    'vendor/lib64/hw/com.qti.chi.override.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'vendor/lib64/hw/camera.qcom.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'mona',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'mojin', module.vendor)
    utils.run()