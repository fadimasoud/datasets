# coding=utf-8
# Copyright 2019 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The rockyou dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """\
"""

_DESCRIPTION = """\
This dataset contains 14,344,391 passwords that were leaked or stolen from from various sites. The author of this dataset states that "I'm hosting them because it seems like nobody else does (hopefully it isn't because hosting them is illegal :)). Naturally, I'm not the one who stole these; I simply found them online, removed any names/email addresses/etc.". This dataset is used to train Machine Learning models for password guessing and cracking.
"""

_DOWNLOAD_URL = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"


class RockYou(tfds.core.GeneratorBasedBuilder):
  """This dataset contains passwords that were leaked or stolen from from various sites."""
  # Version history:
  # 2.0.0: S3 (new shuffling, sharding and slicing mechanism).
  # 1.0.0: Initial version.
  
  VERSION = tfds.core.Version("1.0.0",
                              experiments={tfds.core.Experiment.S3: False})

  SUPPORTED_VERSIONS = [
      tfds.core.Version("2.0.0"),
  ]

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "password":
                tfds.features.Text(encoder=tfds.features.text.ByteTextEncoder()
                                  ),
        }),
        supervised_keys=None,
        urls=["https://wiki.skullsecurity.org/Passwords"],
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    dl_path = dl_manager.download(_DOWNLOAD_URL)
    return [
        tfds.core.SplitGenerator(
            name="train",
            num_shards=1,
            gen_kwargs={
                "path": dl_path,
            },
        )
    ]

  def _generate_examples(self, path):

    with tf.io.gfile.GFile(path, "rb") as f:
      blines = f.readlines()

    for i, bline in enumerate(blines):
      record = {
          "password": bline.strip(),
      }
      if self.version.implements(tfds.core.Experiment.S3):
        yield i, record
      else:
        yield record
