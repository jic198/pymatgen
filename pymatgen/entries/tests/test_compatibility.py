# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

import warnings

"""
Created on Mar 19, 2012
"""


__author__ = "Shyue Ping Ong, Stephen Dacek"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "Mar 19, 2012"

import os
import unittest

from math import sqrt

from monty.json import MontyDecoder
from pymatgen.entries.compatibility import (
    MaterialsProjectCompatibility,
    MITCompatibility,
    AqueousCorrection,
    MITAqueousCompatibility,
    MaterialsProjectCompatibility2020,
    MaterialsProjectAqueousCompatibility2020,
)
from pymatgen.entries.computed_entries import ComputedEntry, ComputedStructureEntry
from pymatgen import Composition, Lattice, Structure, Element


class MaterialsProjectCompatibilityTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore")
        self.entry1 = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry_sulfide = ComputedEntry(
            "FeS",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry2 = ComputedEntry(
            "Fe3O4",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.entry3 = ComputedEntry(
            "FeO",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.compat = MaterialsProjectCompatibility(check_potcar_hash=False)
        self.ggacompat = MaterialsProjectCompatibility("GGA", check_potcar_hash=False)

    def tearDown(self):
        warnings.simplefilter("default")

    def test_process_entry(self):
        # Correct parameters
        self.assertIsNotNone(self.compat.process_entry(self.entry1))
        self.assertIsNone(self.ggacompat.process_entry(self.entry1))

        # Correct parameters
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": {},
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))
        self.assertIsNotNone(self.ggacompat.process_entry(entry))

        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNotNone(self.compat.process_entry(entry))

    def test_correction_values(self):
        # test_corrections
        self.assertAlmostEqual(
            self.compat.process_entry(self.entry1).correction, -2.733 * 2 - 0.70229 * 3
        )

        entry = ComputedEntry(
            "FeF3",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "F": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE F 08Apr2002",
                        "hash": "180141c33d032bfbfff30b3bea9d23dd",
                    },
                ],
            },
        )
        self.assertIsNotNone(self.compat.process_entry(entry))

        # Check actual correction
        self.assertAlmostEqual(self.compat.process_entry(entry).correction, -2.733)

        self.assertAlmostEqual(
            self.compat.process_entry(self.entry_sulfide).correction, -0.66346
        )

    def test_U_values(self):
        # Wrong U value
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.2, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

        # GGA run of U
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

        # GGA+U run of non-U
        entry = ComputedEntry(
            "Al2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Al": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Al 06Sep2000",
                        "hash": "805c888bbd2793e462311f6a20d873d9",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

        # Materials project should not have a U for sulfides
        entry = ComputedEntry(
            "FeS2",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "S": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "f7f8e4a74a6cbb8d63e41f4373b54df2",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

    def test_wrong_psp(self):
        # Wrong psp
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

    def test_element_processing(self):
        entry = ComputedEntry(
            "O",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": {},
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    }
                ],
                "run_type": "GGA",
            },
        )
        entry = self.compat.process_entry(entry)
        #        self.assertEqual(entry.entry_id, -8)
        self.assertAlmostEqual(entry.energy, -1)
        self.assertAlmostEqual(self.ggacompat.process_entry(entry).energy, -1)

    def test_get_explanation_dict(self):
        compat = MaterialsProjectCompatibility(check_potcar_hash=False)
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        d = compat.get_explanation_dict(entry)
        self.assertEqual("MPRelaxSet Potcar Correction", d["corrections"][0]["name"])

    def test_get_corrections_dict(self):
        compat = MaterialsProjectCompatibility(check_potcar_hash=False)
        ggacompat = MaterialsProjectCompatibility("GGA", check_potcar_hash=False)

        # Correct parameters
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        c = compat.get_corrections_dict(entry)[0]
        self.assertAlmostEqual(c["MP Anion Correction"], -2.10687)
        self.assertAlmostEqual(c["MP Advanced Correction"], -5.466)

        entry.parameters["is_hubbard"] = False
        del entry.parameters["hubbards"]
        c = ggacompat.get_corrections_dict(entry)[0]
        self.assertNotIn("MP Advanced Correction", c)

    def test_process_entries(self):
        entries = self.compat.process_entries([self.entry1, self.entry2, self.entry3])
        self.assertEqual(len(entries), 2)

    def test_msonable(self):
        compat_dict = self.compat.as_dict()
        decoder = MontyDecoder()
        temp_compat = decoder.process_decoded(compat_dict)
        print(type(MaterialsProjectCompatibility))
        self.assertIsInstance(temp_compat, MaterialsProjectCompatibility)

    def test_deprecation_warning(self):
        # test that initializing compatibility causes deprecation warning
        with self.assertWarns(DeprecationWarning):
            MaterialsProjectCompatibility(check_potcar_hash=False)


class MaterialsProjectCompatibility2020Test(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore")
        self.entry1 = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry_sulfide = ComputedEntry(
            "FeS",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry2 = ComputedEntry(
            "Fe3O4",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.entry3 = ComputedEntry(
            "FeO",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.compat = MaterialsProjectCompatibility2020(check_potcar_hash=False)
        self.ggacompat = MaterialsProjectCompatibility2020(
            "GGA", check_potcar_hash=False
        )

    def tearDown(self):
        warnings.simplefilter("default")

    def test_process_entry(self):
        # Correct parameters
        self.assertIsNotNone(self.compat.process_entry(self.entry1))
        self.assertIsNone(self.ggacompat.process_entry(self.entry1))

        # Correct parameters
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": {},
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))
        self.assertIsNotNone(self.ggacompat.process_entry(entry))

        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNotNone(self.compat.process_entry(entry))

    def test_correction_values(self):
        # test_corrections
        self.assertAlmostEqual(
            self.compat.process_entry(self.entry1).correction, -2.231 * 2 - 0.721 * 3
        )

        entry = ComputedEntry(
            "FeF3",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "F": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE F 08Apr2002",
                        "hash": "180141c33d032bfbfff30b3bea9d23dd",
                    },
                ],
            },
        )
        self.assertIsNotNone(self.compat.process_entry(entry))

        # Check actual correction
        self.assertAlmostEqual(
            self.compat.process_entry(entry).correction, -0.46 * 3 + -2.231
        )

        self.assertAlmostEqual(
            self.compat.process_entry(self.entry_sulfide).correction, -0.633
        )

    def test_U_values(self):
        # Wrong U value
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.2, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

        # GGA run of U
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

        # GGA+U run of non-U
        entry = ComputedEntry(
            "Al2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Al": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Al 06Sep2000",
                        "hash": "805c888bbd2793e462311f6a20d873d9",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

        # Materials project should not have a U for sulfides
        entry = ComputedEntry(
            "FeS2",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "S": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "f7f8e4a74a6cbb8d63e41f4373b54df2",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

    def test_wrong_psp(self):
        # Wrong psp
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

    def test_element_processing(self):
        entry = ComputedEntry(
            "O",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": {},
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    }
                ],
                "run_type": "GGA",
            },
        )
        entry = self.compat.process_entry(entry)
        #        self.assertEqual(entry.entry_id, -8)
        self.assertAlmostEqual(entry.energy, -1)
        self.assertAlmostEqual(self.ggacompat.process_entry(entry).energy, -1)

    def test_get_explanation_dict(self):
        compat = MaterialsProjectCompatibility(check_potcar_hash=False)
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        d = compat.get_explanation_dict(entry)
        self.assertEqual("MPRelaxSet Potcar Correction", d["corrections"][0]["name"])

    def test_get_corrections_dict(self):
        compat = MaterialsProjectCompatibility2020(check_potcar_hash=False)
        ggacompat = MaterialsProjectCompatibility2020("GGA", check_potcar_hash=False)

        # Correct parameters
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        c, e = compat.get_corrections_dict(entry)
        self.assertAlmostEqual(c["MP Composition Correction"], -0.721 * 3)
        self.assertAlmostEqual(c["MP Advanced Correction"], -2.231 * 2)
        self.assertAlmostEqual(e["MP Composition Correction"], 0.0016 * 3)
        self.assertAlmostEqual(e["MP Advanced Correction"], 0.0079 * 2)

        entry.parameters["is_hubbard"] = False
        del entry.parameters["hubbards"]
        c, e = ggacompat.get_corrections_dict(entry)
        self.assertNotIn("test Advanced Correction", c)

    def test_process_entries(self):
        entries = self.compat.process_entries([self.entry1, self.entry2, self.entry3])
        self.assertEqual(len(entries), 2)

    def test_msonable(self):
        compat_dict = self.compat.as_dict()
        decoder = MontyDecoder()
        temp_compat = decoder.process_decoded(compat_dict)
        self.assertIsInstance(temp_compat, MaterialsProjectCompatibility2020)


class MITCompatibilityTest(unittest.TestCase):
    def tearDown(self):
        warnings.simplefilter("default")

    def setUp(self):
        warnings.simplefilter("ignore")
        self.compat = MITCompatibility(check_potcar_hash=True)
        self.ggacompat = MITCompatibility("GGA", check_potcar_hash=True)
        self.entry_O = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry_F = ComputedEntry(
            "FeF3",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "F": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE F 08Apr2002",
                        "hash": "180141c33d032bfbfff30b3bea9d23dd",
                    },
                ],
            },
        )
        self.entry_S = ComputedEntry(
            "FeS2",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 1.9, "S": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "d368db6899d8839859bbee4811a42a88",
                    },
                ],
            },
        )

    def test_process_entry(self):
        # Correct parameters
        self.assertIsNotNone(self.compat.process_entry(self.entry_O))
        self.assertIsNotNone(self.compat.process_entry(self.entry_F))

    def test_correction_value(self):
        # Check actual correction
        self.assertAlmostEqual(
            self.compat.process_entry(self.entry_O).correction, -1.723 * 2 - 0.66975 * 3
        )
        self.assertAlmostEqual(
            self.compat.process_entry(self.entry_F).correction, -1.723
        )
        self.assertAlmostEqual(
            self.compat.process_entry(self.entry_S).correction, -1.113
        )

    def test_U_value(self):
        # MIT should have a U value for Fe containing sulfides
        self.assertIsNotNone(self.compat.process_entry(self.entry_S))

        # MIT should not have a U value for Ni containing sulfides
        entry = ComputedEntry(
            "NiS2",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Ni": 1.9, "S": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Ni 06Sep2000",
                        "hash": "653f5772e68b2c7fd87ffd1086c0d710",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "d368db6899d8839859bbee4811a42a88",
                    },
                ],
            },
        )

        self.assertIsNone(self.compat.process_entry(entry))

        entry = ComputedEntry(
            "NiS2",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Ni 06Sep2000",
                        "hash": "653f5772e68b2c7fd87ffd1086c0d710",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "d368db6899d8839859bbee4811a42a88",
                    },
                ],
            },
        )

        self.assertIsNotNone(self.ggacompat.process_entry(entry))

    def test_wrong_U_value(self):
        # Wrong U value
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.2, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.assertIsNone(self.compat.process_entry(entry))

        # GGA run
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))
        self.assertIsNotNone(self.ggacompat.process_entry(entry))

    def test_wrong_psp(self):
        # Wrong psp
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

    def test_element_processing(self):
        # Testing processing of elements.
        entry = ComputedEntry(
            "O",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "hubbards": {},
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    }
                ],
                "run_type": "GGA",
            },
        )
        entry = self.compat.process_entry(entry)
        self.assertAlmostEqual(entry.energy, -1)

    def test_same_potcar_symbol(self):
        # Same symbol different hash thus a different potcar
        # Correct Hash Correct Symbol
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "9530da8244e4dac17580869b4adab115",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        # Incorrect Hash Correct Symbol
        entry2 = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {"titel": "PAW_PBE Fe 06Sep2000", "hash": "DifferentHash"},
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        compat = MITCompatibility()
        self.assertEqual(len(compat.process_entries([entry, entry2])), 2)
        self.assertEqual(len(self.compat.process_entries([entry, entry2])), 1)

    def test_revert_to_symbols(self):
        # Test that you can revert to potcar_symbols if potcar_spec is not present
        compat = MITCompatibility()
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_symbols": ["PAW_PBE Fe 06Sep2000", "PAW_PBE O 08Apr2002"],
            },
        )

        self.assertIsNotNone(compat.process_entry(entry))
        # raise if check_potcar_hash is set
        self.assertRaises(ValueError, self.compat.process_entry, entry)

    def test_potcar_doenst_match_structure(self):
        compat = MITCompatibility()
        entry = ComputedEntry(
            "Li2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_symbols": ["PAW_PBE Fe_pv 06Sep2000", "PAW_PBE O 08Apr2002"],
            },
        )

        self.assertIsNone(compat.process_entry(entry))

    def test_potcar_spec_is_none(self):
        compat = MITCompatibility(check_potcar_hash=True)
        entry = ComputedEntry(
            "Li2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [None, None],
            },
        )

        self.assertIsNone(compat.process_entry(entry))

    def test_get_explanation_dict(self):
        compat = MITCompatibility(check_potcar_hash=False)
        entry = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 4.0, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )
        d = compat.get_explanation_dict(entry)
        self.assertEqual("MITRelaxSet Potcar Correction", d["corrections"][0]["name"])

    def test_msonable(self):
        compat_dict = self.compat.as_dict()
        decoder = MontyDecoder()
        temp_compat = decoder.process_decoded(compat_dict)
        self.assertIsInstance(temp_compat, MITCompatibility)

    def test_deprecation_warning(self):
        # test that initializing compatibility causes deprecation warning
        with self.assertWarns(DeprecationWarning):
            MITCompatibility(check_potcar_hash=True)


class OxideTypeCorrectionTest(unittest.TestCase):
    def setUp(self):
        self.compat = MITCompatibility(check_potcar_hash=True)

    def test_no_struct_compat(self):
        lio2_entry_nostruct = ComputedEntry(
            Composition("Li2O4"),
            -3,
            data={"oxide_type": "superoxide"},
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        lio2_entry_corrected = self.compat.process_entry(lio2_entry_nostruct)
        self.assertAlmostEqual(lio2_entry_corrected.energy, -3 - 0.13893 * 4, 4)

    def test_process_entry_superoxide(self):
        el_li = Element("Li")
        el_o = Element("O")
        latt = Lattice(
            [[3.985034, 0.0, 0.0], [0.0, 4.881506, 0.0], [0.0, 0.0, 2.959824]]
        )
        elts = [el_li, el_li, el_o, el_o, el_o, el_o]
        coords = list()
        coords.append([0.500000, 0.500000, 0.500000])
        coords.append([0.0, 0.0, 0.0])
        coords.append([0.632568, 0.085090, 0.500000])
        coords.append([0.367432, 0.914910, 0.500000])
        coords.append([0.132568, 0.414910, 0.000000])
        coords.append([0.867432, 0.585090, 0.000000])
        struct = Structure(latt, elts, coords)
        lio2_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        lio2_entry_corrected = self.compat.process_entry(lio2_entry)
        self.assertAlmostEqual(lio2_entry_corrected.energy, -3 - 0.13893 * 4, 4)

    def test_process_entry_peroxide(self):
        latt = Lattice.from_parameters(
            3.159597, 3.159572, 7.685205, 89.999884, 89.999674, 60.000510
        )
        el_li = Element("Li")
        el_o = Element("O")
        elts = [el_li, el_li, el_li, el_li, el_o, el_o, el_o, el_o]
        coords = [
            [0.666656, 0.666705, 0.750001],
            [0.333342, 0.333378, 0.250001],
            [0.000001, 0.000041, 0.500001],
            [0.000001, 0.000021, 0.000001],
            [0.333347, 0.333332, 0.649191],
            [0.333322, 0.333353, 0.850803],
            [0.666666, 0.666686, 0.350813],
            [0.666665, 0.666684, 0.149189],
        ]
        struct = Structure(latt, elts, coords)
        li2o2_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        li2o2_entry_corrected = self.compat.process_entry(li2o2_entry)
        self.assertAlmostEqual(li2o2_entry_corrected.energy, -3 - 0.44317 * 4, 4)

    def test_process_entry_ozonide(self):
        el_li = Element("Li")
        el_o = Element("O")
        elts = [el_li, el_o, el_o, el_o]
        latt = Lattice.from_parameters(
            3.999911, 3.999911, 3.999911, 133.847504, 102.228244, 95.477342
        )
        coords = [
            [0.513004, 0.513004, 1.000000],
            [0.017616, 0.017616, 0.000000],
            [0.649993, 0.874790, 0.775203],
            [0.099587, 0.874790, 0.224797],
        ]
        struct = Structure(latt, elts, coords)
        lio3_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        lio3_entry_corrected = self.compat.process_entry(lio3_entry)
        self.assertAlmostEqual(lio3_entry_corrected.energy, -3.0)

    def test_process_entry_oxide(self):
        el_li = Element("Li")
        el_o = Element("O")
        elts = [el_li, el_li, el_o]
        latt = Lattice.from_parameters(3.278, 3.278, 3.278, 60, 60, 60)
        coords = [[0.25, 0.25, 0.25], [0.75, 0.75, 0.75], [0.0, 0.0, 0.0]]
        struct = Structure(latt, elts, coords)
        li2o_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        li2o_entry_corrected = self.compat.process_entry(li2o_entry)
        self.assertAlmostEqual(li2o_entry_corrected.energy, -3.0 - 0.66975, 4)


class SulfideTypeCorrection2020Test(unittest.TestCase):
    def setUp(self):
        self.compat = MaterialsProjectCompatibility2020(check_potcar_hash=False)

    def test_struct_no_struct(self):
        # Processing an Entry should produce the same correction whether or not
        # that entry has a Structure attached to it.
        # This test will FAIL in previous version of pymatgen in which
        # 'polysulfide' was a valid output from structure_analyzer.sulfide_type()

        # Na2S2, entry mp-2400, with and without structure
        from collections import defaultdict

        entry_struct_as_dict = {
            "@module": "pymatgen.entries.computed_entries",
            "@class": "ComputedStructureEntry",
            "energy": -28.42580746,
            "composition": defaultdict(float, {"Na": 4.0, "S": 4.0}),
            "correction": 0,
            "parameters": {
                "run_type": "GGA",
                "is_hubbard": False,
                "pseudo_potential": {
                    "functional": "PBE",
                    "labels": ["Na_pv", "S"],
                    "pot_type": "paw",
                },
                "hubbards": {},
                "potcar_symbols": ["PBE Na_pv", "PBE S"],
                "oxide_type": "None",
            },
            "data": {"oxide_type": "None"},
            "entry_id": "mp-2400",
            "structure": {
                "@module": "pymatgen.core.structure",
                "@class": "Structure",
                "charge": None,
                "lattice": {
                    "matrix": [
                        [4.5143094, 0.0, 0.0],
                        [-2.2571547, 3.90950662, 0.0],
                        [0.0, 0.0, 10.28414905],
                    ],
                    "a": 4.5143094,
                    "b": 4.514309399183436,
                    "c": 10.28414905,
                    "alpha": 90.0,
                    "beta": 90.0,
                    "gamma": 120.00000000598358,
                    "volume": 181.50209256783256,
                },
                "sites": [
                    {
                        "species": [{"element": "Na", "occu": 1}],
                        "abc": [0.0, 0.0, 0.0],
                        "xyz": [0.0, 0.0, 0.0],
                        "label": "Na",
                        "properties": {"magmom": 0.0},
                    },
                    {
                        "species": [{"element": "Na", "occu": 1}],
                        "abc": [0.0, 0.0, 0.5],
                        "xyz": [0.0, 0.0, 5.142074525],
                        "label": "Na",
                        "properties": {"magmom": 0.0},
                    },
                    {
                        "species": [{"element": "Na", "occu": 1}],
                        "abc": [0.33333333, 0.66666667, 0.25],
                        "xyz": [
                            -2.2571547075855847e-08,
                            2.6063377596983557,
                            2.5710372625,
                        ],
                        "label": "Na",
                        "properties": {"magmom": 0.0},
                    },
                    {
                        "species": [{"element": "Na", "occu": 1}],
                        "abc": [0.66666667, 0.33333333, 0.75],
                        "xyz": [2.2571547225715474, 1.3031688603016447, 7.7131117875],
                        "label": "Na",
                        "properties": {"magmom": 0.0},
                    },
                    {
                        "species": [{"element": "S", "occu": 1}],
                        "abc": [0.33333333, 0.66666667, 0.644551],
                        "xyz": [
                            -2.2571547075855847e-08,
                            2.6063377596983557,
                            6.62865855432655,
                        ],
                        "label": "S",
                        "properties": {"magmom": 0.0},
                    },
                    {
                        "species": [{"element": "S", "occu": 1}],
                        "abc": [0.66666667, 0.33333333, 0.144551],
                        "xyz": [
                            2.2571547225715474,
                            1.3031688603016447,
                            1.4865840293265502,
                        ],
                        "label": "S",
                        "properties": {"magmom": 0.0},
                    },
                    {
                        "species": [{"element": "S", "occu": 1}],
                        "abc": [0.66666667, 0.33333333, 0.355449],
                        "xyz": [
                            2.2571547225715474,
                            1.3031688603016447,
                            3.65549049567345,
                        ],
                        "label": "S",
                        "properties": {"magmom": 0.0},
                    },
                    {
                        "species": [{"element": "S", "occu": 1}],
                        "abc": [0.33333333, 0.66666667, 0.855449],
                        "xyz": [
                            -2.2571547075855847e-08,
                            2.6063377596983557,
                            8.79756502067345,
                        ],
                        "label": "S",
                        "properties": {"magmom": 0.0},
                    },
                ],
            },
        }

        entry_no_struct_as_dict = {
            "@module": "pymatgen.entries.computed_entries",
            "@class": "ComputedEntry",
            "energy": -28.42580746,
            "composition": defaultdict(float, {"Na": 4.0, "S": 4.0}),
            "correction": -2.65384,
            "parameters": {
                "run_type": "GGA",
                "is_hubbard": False,
                "pseudo_potential": {
                    "functional": "PBE",
                    "labels": ["Na_pv", "S"],
                    "pot_type": "paw",
                },
                "hubbards": {},
                "potcar_symbols": ["PBE Na_pv", "PBE S"],
                "oxide_type": "None",
            },
            "data": {"oxide_type": "None"},
            "entry_id": "mp-2400",
        }

        na2s2_entry_struct = ComputedStructureEntry.from_dict(entry_struct_as_dict)
        na2s2_entry_nostruct = ComputedEntry.from_dict(entry_no_struct_as_dict)

        struct_corrected = self.compat.process_entry(na2s2_entry_struct)
        nostruct_corrected = self.compat.process_entry(na2s2_entry_nostruct)

        self.assertAlmostEqual(
            struct_corrected.correction, nostruct_corrected.correction, 4
        )


class OxideTypeCorrectionNoPeroxideCorrTest(unittest.TestCase):
    def setUp(self):
        self.compat = MITCompatibility(correct_peroxide=False)

    def test_oxide_energy_corr(self):
        el_li = Element("Li")
        el_o = Element("O")
        elts = [el_li, el_li, el_o]
        latt = Lattice.from_parameters(3.278, 3.278, 3.278, 60, 60, 60)
        coords = [[0.25, 0.25, 0.25], [0.75, 0.75, 0.75], [0.0, 0.0, 0.0]]
        struct = Structure(latt, elts, coords)
        li2o_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        li2o_entry_corrected = self.compat.process_entry(li2o_entry)
        self.assertAlmostEqual(li2o_entry_corrected.energy, -3.0 - 0.66975, 4)

    def test_peroxide_energy_corr(self):
        latt = Lattice.from_parameters(
            3.159597, 3.159572, 7.685205, 89.999884, 89.999674, 60.000510
        )
        el_li = Element("Li")
        el_o = Element("O")
        elts = [el_li, el_li, el_li, el_li, el_o, el_o, el_o, el_o]
        coords = [
            [0.666656, 0.666705, 0.750001],
            [0.333342, 0.333378, 0.250001],
            [0.000001, 0.000041, 0.500001],
            [0.000001, 0.000021, 0.000001],
            [0.333347, 0.333332, 0.649191],
            [0.333322, 0.333353, 0.850803],
            [0.666666, 0.666686, 0.350813],
            [0.666665, 0.666684, 0.149189],
        ]
        struct = Structure(latt, elts, coords)
        li2o2_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        li2o2_entry_corrected = self.compat.process_entry(li2o2_entry)
        self.assertRaises(
            AssertionError,
            self.assertAlmostEqual,
            *(li2o2_entry_corrected.energy, -3 - 0.44317 * 4, 4)
        )
        self.assertAlmostEqual(li2o2_entry_corrected.energy, -3 - 0.66975 * 4, 4)

    def test_ozonide(self):
        el_li = Element("Li")
        el_o = Element("O")
        elts = [el_li, el_o, el_o, el_o]
        latt = Lattice.from_parameters(
            3.999911, 3.999911, 3.999911, 133.847504, 102.228244, 95.477342
        )
        coords = [
            [0.513004, 0.513004, 1.000000],
            [0.017616, 0.017616, 0.000000],
            [0.649993, 0.874790, 0.775203],
            [0.099587, 0.874790, 0.224797],
        ]
        struct = Structure(latt, elts, coords)
        lio3_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        lio3_entry_corrected = self.compat.process_entry(lio3_entry)
        self.assertAlmostEqual(lio3_entry_corrected.energy, -3.0 - 3 * 0.66975)


class MPAqueousCorrection2020Test(unittest.TestCase):
    def setUp(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(module_dir, os.path.pardir, "MPCompatibility2020.yaml")
        self.corr = AqueousCorrection(fp)

        self.compat = MaterialsProjectCompatibility2020(check_potcar_hash=False)
        self.aqcompat = MaterialsProjectAqueousCompatibility2020(
            check_potcar_hash=False
        )
        self.aqcorr = AqueousCorrection(fp)

    def test_compound_energy(self):

        O2_entry = self.corr.correct_entry(
            ComputedEntry(Composition("O2"), -4.9276 * 2)  # mp-12957
        )
        H2_entry = self.corr.correct_entry(ComputedEntry(Composition("H2"), 3))
        H2O_entry = self.corr.correct_entry(ComputedEntry(Composition("H2O"), 3))
        H2O_formation_energy = H2O_entry.energy - (
            H2_entry.energy + O2_entry.energy / 2.0
        )
        self.assertAlmostEqual(H2O_formation_energy, -2.4583, 2)

        entry = ComputedEntry(Composition("H2O"), -16)
        entry = self.corr.correct_entry(entry)
        self.assertAlmostEqual(entry.energy, -15.7581, 4)

        entry = ComputedEntry(Composition("H2O"), -24)
        entry = self.corr.correct_entry(entry)
        self.assertAlmostEqual(entry.energy, -15.7581, 4)

        entry = ComputedEntry(Composition("Cl"), -24)
        entry = self.corr.correct_entry(entry)
        self.assertAlmostEqual(entry.energy, -24.344373, 4)

    def test_aqueous_compat(self):

        el_li = Element("Li")
        el_o = Element("O")
        el_h = Element("H")
        latt = Lattice.from_parameters(
            3.565276, 3.565276, 4.384277, 90.000000, 90.000000, 90.000000
        )
        elts = [el_h, el_h, el_li, el_li, el_o, el_o]
        coords = [
            [0.000000, 0.500000, 0.413969],
            [0.500000, 0.000000, 0.586031],
            [0.000000, 0.000000, 0.000000],
            [0.500000, 0.500000, 0.000000],
            [0.000000, 0.500000, 0.192672],
            [0.500000, 0.000000, 0.807328],
        ]
        struct = Structure(latt, elts, coords)
        lioh_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li_sv 17Jan2003",  # date/hash from mit potcar_spec
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                    {
                        "titel": "PAW_PBE H 15Jun2001",
                        "hash": "bb43c666e3d36577264afe07669e9582",
                    },
                ],
            },
        )
        lioh_entry_compat = self.compat.process_entry(lioh_entry)
        lioh_entry_compat_aqcorr = self.aqcorr.correct_entry(lioh_entry_compat)
        lioh_entry_aqcompat = self.aqcompat.process_entry(lioh_entry)
        self.assertAlmostEqual(
            lioh_entry_compat_aqcorr.energy, lioh_entry_aqcompat.energy, 4
        )


class AqueousCorrectionTest(unittest.TestCase):
    def setUp(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(module_dir, os.path.pardir, "MITCompatibility.yaml")
        self.corr = AqueousCorrection(fp)

    def test_compound_energy(self):
        O2_entry = self.corr.correct_entry(
            ComputedEntry(Composition("O2"), -4.9355 * 2)
        )
        H2_entry = self.corr.correct_entry(ComputedEntry(Composition("H2"), 3))
        H2O_entry = self.corr.correct_entry(ComputedEntry(Composition("H2O"), 3))
        H2O_formation_energy = H2O_entry.energy - (
            H2_entry.energy + O2_entry.energy / 2.0
        )
        self.assertAlmostEqual(H2O_formation_energy, -2.46, 2)

        entry = ComputedEntry(Composition("H2O"), -16)
        entry = self.corr.correct_entry(entry)
        self.assertAlmostEqual(entry.energy, -14.916, 4)

        entry = ComputedEntry(Composition("H2O"), -24)
        entry = self.corr.correct_entry(entry)
        self.assertAlmostEqual(entry.energy, -14.916, 4)

        entry = ComputedEntry(Composition("Cl"), -24)
        entry = self.corr.correct_entry(entry)
        self.assertAlmostEqual(entry.energy, -24.344373, 4)


class MITAqueousCompatibilityTest(unittest.TestCase):
    def setUp(self):
        self.compat = MITCompatibility(check_potcar_hash=True)
        self.aqcompat = MITAqueousCompatibility(check_potcar_hash=True)
        module_dir = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(module_dir, os.path.pardir, "MITCompatibility.yaml")
        self.aqcorr = AqueousCorrection(fp)

    def test_aqueous_compat(self):

        el_li = Element("Li")
        el_o = Element("O")
        el_h = Element("H")
        latt = Lattice.from_parameters(
            3.565276, 3.565276, 4.384277, 90.000000, 90.000000, 90.000000
        )
        elts = [el_h, el_h, el_li, el_li, el_o, el_o]
        coords = [
            [0.000000, 0.500000, 0.413969],
            [0.500000, 0.000000, 0.586031],
            [0.000000, 0.000000, 0.000000],
            [0.500000, 0.500000, 0.000000],
            [0.000000, 0.500000, 0.192672],
            [0.500000, 0.000000, 0.807328],
        ]
        struct = Structure(latt, elts, coords)
        lioh_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li 17Jan2003",
                        "hash": "65e83282d1707ec078c1012afbd05be8",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                    {
                        "titel": "PAW_PBE H 15Jun2001",
                        "hash": "bb43c666e3d36577264afe07669e9582",
                    },
                ],
            },
        )
        lioh_entry_compat = self.compat.process_entry(lioh_entry)
        lioh_entry_compat_aqcorr = self.aqcorr.correct_entry(lioh_entry_compat)
        lioh_entry_aqcompat = self.aqcompat.process_entry(lioh_entry)
        self.assertAlmostEqual(
            lioh_entry_compat_aqcorr.energy, lioh_entry_aqcompat.energy, 4
        )

    def test_potcar_doenst_match_structure(self):
        compat = MITCompatibility()
        el_li = Element("Li")
        el_o = Element("O")
        el_h = Element("H")
        latt = Lattice.from_parameters(
            3.565276, 3.565276, 4.384277, 90.000000, 90.000000, 90.000000
        )
        elts = [el_h, el_h, el_li, el_li, el_o, el_o]
        coords = [
            [0.000000, 0.500000, 0.413969],
            [0.500000, 0.000000, 0.586031],
            [0.000000, 0.000000, 0.000000],
            [0.500000, 0.500000, 0.000000],
            [0.000000, 0.500000, 0.192672],
            [0.500000, 0.000000, 0.807328],
        ]
        struct = Structure(latt, elts, coords)

        lioh_entry = ComputedStructureEntry(
            struct,
            -3,
            parameters={
                "is_hubbard": False,
                "hubbards": None,
                "run_type": "GGA",
                "potcar_symbols": [
                    "PAW_PBE Fe 17Jan2003",
                    "PAW_PBE O 08Apr2002",
                    "PAW_PBE H 15Jun2001",
                ],
            },
        )

        self.assertIsNone(compat.process_entry(lioh_entry))

    def test_msonable(self):
        compat_dict = self.aqcompat.as_dict()
        decoder = MontyDecoder()
        temp_compat = decoder.process_decoded(compat_dict)
        self.assertIsInstance(temp_compat, MITAqueousCompatibility)

    def test_dont_error_on_weird_elements(self):
        entry = ComputedEntry(
            "AmSi",
            -1,
            0.0,
            parameters={
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Am 08May2007",
                        "hash": "ed5eebd8a143e35a0c19e9f8a2c42a93",
                    },
                    {
                        "titel": "PAW_PBE Si 05Jan2001",
                        "hash": "b2b0ea6feb62e7cde209616683b8f7f5",
                    },
                ]
            },
        )
        self.assertIsNone(self.compat.process_entry(entry))

    def test_deprecation_warning(self):
        # test that initializing compatibility causes deprecation warning
        with self.assertWarns(DeprecationWarning):
            MITAqueousCompatibility(check_potcar_hash=True)


class CorrectionErrorsCompatibility2020Test(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore")
        self.compat = MaterialsProjectCompatibility2020()

        self.entry1 = ComputedEntry(
            "Fe2O3",
            -1,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry_sulfide = ComputedEntry(
            "FeS",
            -1,
            0.0,
            parameters={
                "is_hubbard": False,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE S 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry2 = ComputedEntry(
            "Fe3O4",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "O": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE O 08Apr2002",
                        "hash": "7a25bc5b9a5393f46600a4939d357982",
                    },
                ],
            },
        )

        self.entry_fluoride = ComputedEntry(
            "FeF3",
            -2,
            0.0,
            parameters={
                "is_hubbard": True,
                "hubbards": {"Fe": 5.3, "F": 0},
                "run_type": "GGA+U",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Fe_pv 06Sep2000",
                        "hash": "994537de5c4122b7f1b77fb604476db4",
                    },
                    {
                        "titel": "PAW_PBE F 08Apr2002",
                        "hash": "180141c33d032bfbfff30b3bea9d23dd",
                    },
                ],
            },
        )

        self.entry_hydride = ComputedEntry(
            "LiH",
            -2,
            0.0,
            parameters={
                "is_hubbard": False,
                "run_type": "GGA",
                "potcar_spec": [
                    {
                        "titel": "PAW_PBE Li_sv 10Sep2004",
                        "hash": "8245d7383d7556214082aa40a887cd96",
                    },
                    {
                        "titel": "PAW_PBE H 15Jun2001",
                        "hash": "bb43c666e3d36577264afe07669e9582",
                    },
                ],
            },
        )

    def tearDown(self):
        warnings.simplefilter("default")

    def test_errors(self):
        entry1_corrected = self.compat.process_entry(self.entry1)
        self.assertAlmostEqual(
            entry1_corrected.data["correction_uncertainty"],
            sqrt((2 * 0.0079) ** 2 + (3 * 0.0016) ** 2),
        )

        entry2_corrected = self.compat.process_entry(self.entry2)
        self.assertAlmostEqual(
            entry2_corrected.data["correction_uncertainty"],
            sqrt((3 * 0.0079) ** 2 + (4 * 0.0016) ** 2),
        )

        entry_sulfide_corrected = self.compat.process_entry(self.entry_sulfide)
        self.assertAlmostEqual(
            entry_sulfide_corrected.data["correction_uncertainty"], 0.0121
        )

        entry_fluoride_corrected = self.compat.process_entry(self.entry_fluoride)
        self.assertAlmostEqual(
            entry_fluoride_corrected.data["correction_uncertainty"],
            sqrt((3 * 0.0025) ** 2 + 0.0079 ** 2),
        )

        entry_hydride_corrected = self.compat.process_entry(self.entry_hydride)
        self.assertAlmostEqual(
            entry_hydride_corrected.data["correction_uncertainty"], 0.0013
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
