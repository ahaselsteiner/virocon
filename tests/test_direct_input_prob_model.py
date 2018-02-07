from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from enviro.forms import VariableNumber, VariablesForm

class UploadFileTestCase(TestCase):
    def setUp(self):
        # create a user
        self.client = Client()
        self.client.post(reverse('user:create'),
                           {'username' : 'max_mustermann',
                            'email': 'max.mustermann@gmail.com',
                            'first_name': 'Max',
                            'last_name': 'Mustermann',
                            'organisation': 'Musterfirma',
                            'type_of_use': 'commercial',
                            'password1' : 'AnJaKaTo2018',
                            'password2': 'AnJaKaTo2018'})

        # create a measurement file
        test_files_path = os.path.abspath(os.path.join(
            os.path.dirname( __file__), r'test_files/'))
        file_name = '1yeardata_vanem2012pdf_withHeader.csv'

        # thanks to: https://stackoverflow.com/questions/2473392/unit-testing-
        # a-django-form-with-a-filefield
        test_file = open(os.path.join(test_files_path , file_name), 'rb')
        test_file_simple_uploaded = SimpleUploadedFile(test_file.name,
                                                       test_file.read())
        self.client.post(reverse('enviro:measurefiles-add'),
                                    {'title' : file_name,
                                     'measure_file' : test_file_simple_uploaded
                                    })




    def test_direct_input_prob_model(self):
        # open direct input url and check if the html is correct
        response = self.client.post(reverse('enviro:probabilistic_model-add',
                                            args=['02']))
        self.assertContains(response, "The first characer should be "
                                      "capizalized.", status_code=200)

        # create a direct input form
        form = VariableNumber({'variable_number' : '2'})
        self.assertTrue(form.is_valid())

        # create a form containing the information of the model
        form_input_dict = {
                'variable_name_0' : 'significant wave height [m]',
                'variable_symbol_0' : 'Hs',
                'distribution_0' : 'Weibull',
                'scale_0_0' : '2.7',
                'shape_0_0' : '1.5',
                'location_0_0' : '0.9',
                'variable_name_1' : 'peak period [s]',
                'variable_symbol_1' : 'Tp',
                'distribution_1': 'Weibull',
                'scale_dependency_1': '0f2',
                'scale_1_0' : '2.7',
                'scale_1_1' : '2.7',
                'scale_1_2' : '2.7',
                'shape_dependency_1' : '0f1',
                'shape_1_0' : '1.5',
                'shape_1_1' : '1.5',
                'shape_1_2' : '1.5',
                'location_dependency_1': '!None',
                'location_1_0' : '0.9',
                'location_1_1' : '0.9',
                'location_1_2' : '0.9',
                'collection_name' : 'Direct input model'
            }
        form = VariablesForm(data=form_input_dict, variable_count=2)
        self.assertTrue(form.is_valid())

        # test the view method and the html which will be generated
        response = self.client.post(reverse('enviro:probabilistic_model-add',
                                            args=['02']),
                                    form_input_dict,
                                    follow=True)
        self.assertContains(response, "ploaded probabilistic models",
                            status_code=200)