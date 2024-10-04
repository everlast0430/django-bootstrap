from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
	def setUp(self):
		self.client = Client()

	def test_post_list(self):

		# 1.1 블로그 Post 페이지를 연다.
		response = self.client.get('/blog/')
		# 1.2 정상적으로 페이지가 로드돈다. (202)
		self.assertEquals(response.status_code,200)
		# 1.3 페이지의 타이틀에 Blog라는 문구가 뜬다.
		soup = BeautifulSoup(response.content, 'html.parser')
		self.assertIn('Blog', soup.title.text)
		# 1.4 NavBar가 있다.
		navbar = soup.nav
		# 1.5 NavBar에 Blog, About me가 포함되있어야 한다.
		self.assertIn('Blog', navbar.text)
		self.assertIn('About me', navbar.text)

		# 2.1 게시물이 하나도 없을 때,
		# (** Django에서는 기본적으로 테스트할 때, 테스트용 DB를 만들며 그 DB는 아무 데이터도 없는 상황임)
		self.assertEquals(Post.objects.count(), 0)
		# 2.2 메인영역에 "아직 게시물이 없습니다"라는 문구가 나온다.
		main_area = soup.find('div', id='main-area')
		self.assertIn("아직 게시물이 없습니다.", main_area.text)

		# 3.1 게시물이 하나 이상 있을 때,
		post_001 = Post.objects.create(
			title="첫번째 포스트입니다.",
			content="저는 sabrikong입니다.",
		)
		post_002 = Post.objects.create(
			title="두번쨰 포스트입니다.",
			content="저는 삼겹살을 좋아합니다.",
		)
		# 3.2 포스트 목록 페이지를 새로 고침했을 때,
		response = self.client.get('/blog/')
		# 3.2 메인 영역에 해당 포스트가 나타나야 한다.
		soup = BeautifulSoup(response.content, 'html.parser')
		main_area = soup.find('div', id='main-area')
		self.assertIn(post_001.title, main_area.text)
		self.assertIn(post_002.title, main_area.text)
		# 3.4 "아직 게시물이 없습니다"라는 문구가 없어야 한다.
		self.assertNotIn("아직 게시물이 없습니다.", main_area.text)

# get
# assertEqual
# assertIn