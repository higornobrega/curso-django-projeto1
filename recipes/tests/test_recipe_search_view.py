from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewsTest(RecipeTestBase):

    def test_recipe_search_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:search')
        )
        self.assertIs(view.func, views.search)
        
    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?search=test'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        
    def test_recipe_search_raise_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?search=Teste'
        response = self.client.get(url)
        
        self.assertIn(
            'Search for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )