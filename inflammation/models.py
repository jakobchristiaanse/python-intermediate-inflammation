"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""
from functools import reduce

import numpy as np


class Observation:
    """
    Class representing a patient's observations.

    Attributes:
        day
        value
    """

    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return str(self.value)


class Person:
    """
    Class representing a person.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Patient(Person):
    """A patient in an inflammation study."""

    def __init__(self, name):
        super().__init__(name)
        self.observations = []

    def add_observation(self, value, day=None):
        if day is None:
            try:
                day = self.observations[-1].day + 1

            except IndexError:
                day = 0

        new_observation = Observation(day, value)

        self.observations.append(new_observation)
        return new_observation


class Doctor(Person):
    """A doctor in an inflammation study."""

    def __init__(self, name):
        super().__init__(name)
        self.patients = []

    def add_patient(self, patient):

        if isinstance(patient, Patient):
            new_patient = patient
        else:
            new_patient = Patient(patient)

        if new_patient not in self.patients:
            self.patients.append(new_patient)
            return new_patient
        else:
            print('Patient with name %s already in Doctor %s\'s list.' % (patient, self.name))

def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """
    Calculate the daily mean of a 2D inflammation data array.

    :param data: 2D inflammation data array
    :returns: daily mean
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """
    Calculate the daily max of a 2D inflammation data array.

    :param data: 2D inflammation data array
    :returns: daily max
    """
    return np.max(data, axis=0)


def daily_min(data):
    """
    Calculate the daily min of a 2D inflammation data array.

    :param data: 2D inflammation data array
    :returns: daily min
    """
    return np.min(data, axis=0)


def daily_std(data):
    """
    Calculate the daily standard deviation of a 2D inflammation data array.

    :param data: 2D inflammation data array
    :returns: daily standard deviation
    """
    return np.std(data, axis=0)


def patient_normalise(data):
    """
    Normalise patient data from a 2D inflammation data array.
    NaN values are ignored, and normalised to 0.
    Negative values are rounded to 0.

    :param data: 2D inflammation data array
    :returns: normalised patient data
    """
    if np.any(data < 0):
        raise ValueError('Inflammation values should not be negative')
    if not isinstance(data, np.ndarray):
        raise TypeError('Inflammation data should be an Numpy nd-array')

    max_val = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / max_val[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised


def daily_above_threshold(data, patient_nr, threshold):
    """
    Determine the number of days a patient's inflammation data is above a threshold.

    :param data: 2D inflammation data array
    :param patient_nr: patient index
    :param threshold: daily threshold
    :returns: True if patient's daily inflammation data is above a threshold'
    """
    bools = list(map(lambda x: x > threshold, data[patient_nr]))
    int_bools = [int(x) for x in bools]
    return reduce(lambda x, y: x + y, int_bools)
