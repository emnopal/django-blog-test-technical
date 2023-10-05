from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Profile


class AuthUserAbstraction(LoginRequiredMixin):

    def _following(self, user):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.user_id user
                FROM user_auth_profile p
                JOIN user_auth_profile_followers pf ON p.id = pf.profile_id
                JOIN auth_user a on p.user_id = a.id
                WHERE pf.user_id = %s
            """, [user])
            row = cursor.fetchone()
        return row

    def _follower(self, user):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    pf.user_id user
                FROM user_auth_profile p
                JOIN user_auth_profile_followers pf ON p.id = pf.profile_id
                JOIN auth_user a on p.user_id = a.id
                WHERE p.user_id = %s
            """, [user])
            row = cursor.fetchone()
        return row

    def get_following(self, user=None):
        user = self.request.user.id if not user else user.id
        follows = self._following(user)
        list_user = []
        if follows:
            for follow in follows:
                follow_profile = Profile.objects.get(user_id=follow)
                list_user.append(follow_profile.user)
        return list_user

    def get_followers(self, user=None):
        user = self.request.user.id if not user else user.id
        follows = self._follower(user)
        list_user = []
        if follows:
            for follow in follows:
                follow_profile = Profile.objects.get(user_id=follow)
                list_user.append(follow_profile.user)
        return list_user

    def number_of_following(self, user=None):
        user = self.request.user.id if not user else user.id
        follows = self._following(user)
        num_user = 0
        if follows:
            for _ in follows:
                num_user += 1
        return num_user

    def number_of_followers(self, user=None):
        user = self.request.user.id if not user else user.id
        follows = self._follower(user)
        num_user = 0
        if follows:
            for _ in follows:
                num_user += 1
        return num_user


class AuthViewAbstraction(AuthUserAbstraction, View):...


class AuthDetailViewAbstraction(AuthUserAbstraction, DetailView):...


class AuthListViewAbstraction(AuthUserAbstraction, ListView):...


class AuthDetailViewAbstraction(AuthUserAbstraction, DetailView):...


class AuthUpdateViewAbstraction(AuthUserAbstraction, UpdateView):...


class AuthCreateViewAbstraction(AuthUserAbstraction, CreateView):...


class AuthDeleteViewAbstraction(AuthUserAbstraction, DeleteView):...
