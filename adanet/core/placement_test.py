# Copyright 2019 The AdaNet Authors. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Distributed placement strategy tests."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
from adanet.core.placement import ReplicationStrategy
from adanet.core.placement import RoundRobinStrategy

import tensorflow as tf


class ReplicationStrategyTest(tf.test.TestCase):

  def test_strategy(self):
    strategy = ReplicationStrategy()
    num_subnetworks = 3
    subnetwork_index = 1
    self.assertTrue(strategy.should_build_ensemble(num_subnetworks))
    self.assertTrue(
        strategy.should_build_subnetwork(num_subnetworks, subnetwork_index))
    self.assertTrue(strategy.should_train_subnetworks(num_subnetworks))


class RoundRobinStrategyTest(parameterized.TestCase, tf.test.TestCase):

  @parameterized.named_parameters({
      "testcase_name": "one_worker_one_subnetwork",
      "num_workers": 1,
      "num_subnetworks": 1,
      "want_should_build_ensemble": [True],
      "want_should_build_subnetwork": [[True]],
      "want_should_train_subnetworks": [True],
  }, {
      "testcase_name": "three_workers_one_subnetworks",
      "num_workers": 3,
      "num_subnetworks": 1,
      "want_should_build_ensemble": [True, True, True],
      "want_should_build_subnetwork": [[True], [True], [True]],
      "want_should_train_subnetworks": [True, True, True],
  }, {
      "testcase_name": "two_workers_one_subnetworks",
      "num_workers": 2,
      "num_subnetworks": 5,
      "want_should_build_ensemble": [True, False],
      "want_should_build_subnetwork": [[True, True, True, True, True],
                                       [True, True, True, True, True]],
      "want_should_train_subnetworks": [False, True],
  }, {
      "testcase_name": "one_worker_three_subnetworks",
      "num_workers": 1,
      "num_subnetworks": 3,
      "want_should_build_ensemble": [True],
      "want_should_build_subnetwork": [[True, True, True]],
      "want_should_train_subnetworks": [True],
  }, {
      "testcase_name": "two_workers_three_subnetworks",
      "num_workers": 2,
      "num_subnetworks": 3,
      "want_should_build_ensemble": [True, False],
      "want_should_build_subnetwork": [
          [True, True, True],
          [True, True, True],
      ],
      "want_should_train_subnetworks": [False, True],
  }, {
      "testcase_name": "three_workers_three_subnetworks",
      "num_workers": 3,
      "num_subnetworks": 3,
      "want_should_build_ensemble": [True, False, False],
      "want_should_build_subnetwork": [
          [True, True, True],
          [True, False, True],
          [False, True, False],
      ],
      "want_should_train_subnetworks": [False, True, True],
  }, {
      "testcase_name":
          "four_workers_three_subnetworks",
      "num_workers":
          4,
      "num_subnetworks":
          3,
      "want_should_build_ensemble":
          [True, False, False, False],
      "want_should_build_subnetwork": [
          [True, True, True],
          [True, False, False],
          [False, True, False],
          [False, False, True],
      ],
      "want_should_train_subnetworks":
          [False, True, True, True],
  }, {
      "testcase_name":
          "five_workers_three_subnetworks",
      "num_workers":
          5,
      "num_subnetworks":
          3,
      "want_should_build_ensemble":
          [True, False, False, False, True],
      "want_should_build_subnetwork": [
          [True, True, True],
          [True, False, False],
          [False, True, False],
          [False, False, True],
          [True, True, True],
      ],
      "want_should_train_subnetworks":
          [False, True, True, True, False],
  }, {
      "testcase_name":
          "six_workers_three_subnetworks",
      "num_workers":
          6,
      "num_subnetworks":
          3,
      "want_should_build_ensemble":
          [True, False, False, False, True, False],
      "want_should_build_subnetwork": [
          [True, True, True],
          [True, False, False],
          [False, True, False],
          [False, False, True],
          [True, True, True],
          [True, True, True],
      ],
      "want_should_train_subnetworks":
          [False, True, True, True, False, True],
  }, {
      "testcase_name":
          "seven_workers_three_subnetworks",
      "num_workers":
          7,
      "num_subnetworks":
          3,
      "want_should_build_ensemble":
          [True, False, False, False, True, False, False],
      "want_should_build_subnetwork": [
          [True, True, True],
          [True, False, False],
          [False, True, False],
          [False, False, True],
          [True, True, True],
          [True, False, True],
          [False, True, False],
      ],
      "want_should_train_subnetworks":
          [False, True, True, True, False, True, True],
  }, {
      "testcase_name":
          "eight_workers_three_subnetworks",
      "num_workers":
          8,
      "num_subnetworks":
          3,
      "want_should_build_ensemble":
          [True, False, False, False, True, False, False, False],
      "want_should_build_subnetwork": [
          [True, True, True],
          [True, False, False],
          [False, True, False],
          [False, False, True],
          [True, True, True],
          [True, False, False],
          [False, True, False],
          [False, False, True],
      ],
      "want_should_train_subnetworks":
          [False, True, True, True, False, True, True, True],
  })
  def test_should_build_ensemble(
      self, num_workers, num_subnetworks, want_should_build_ensemble,
      want_should_build_subnetwork, want_should_train_subnetworks):
    should_build_ensemble = []
    should_build_subnetwork = []
    should_train_subnetworks = []
    for worker_index in range(num_workers):
      strategy = RoundRobinStrategy(num_workers, worker_index)
      should_build_ensemble.append(
          strategy.should_build_ensemble(num_subnetworks))
      should_build_subnetwork.append([])
      should_train_subnetworks.append(
          strategy.should_train_subnetworks(num_subnetworks))
      for subnetwork_index in range(num_subnetworks):
        should_build_subnetwork[-1].append(
            strategy.should_build_subnetwork(num_subnetworks, subnetwork_index))
    self.assertEqual(want_should_build_ensemble, should_build_ensemble)
    self.assertEqual(want_should_build_subnetwork, should_build_subnetwork)
    self.assertEqual(want_should_train_subnetworks, should_train_subnetworks)


if __name__ == "__main__":
  tf.test.main()
