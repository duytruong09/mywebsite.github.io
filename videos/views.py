from django.db.models import Q
from django.shortcuts import render, reverse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import CommentForm
from .models import Video, Comment, Category

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class Index(ListView):
    model = Video
    template_name = 'videos/index.html'
    order_by = '-date_post'


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'thumbnail', 'category']
    template_name = 'videos/create_video.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('videos:video-detail', kwargs={'pk': self.object.pk})


class DetailVideo(DetailView):
    def get(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        categories = Video.objects.filter(category=video.category)[:15]

        form = CommentForm()
        comments = Comment.objects.filter(video=video).order_by('-created_on')
        context = {
            'object': video,
            'comments': comments,
            'categories': categories,
            'form': form,
        }
        return render(request, 'videos/detail_video.html', context)

    def post(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        categories = Video.objects.filter(category=video.category)[:15]

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                user = self.request.user,
                comment = form.cleaned_data['comment'],
                video = video
            )
            comment.save()

        comments = Comment.objects.filter(video=video).order_by('-created_on')
        context = {
            'object': video,
            'comments': comments,
            'categories': categories,
            'form': form
        }
        return render(request, 'videos/detail_video.html', context)


class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description']
    template_name = 'videos/create_video.html'

    def get_success_url(self):
        return reverse('videos:video-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class DeleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'

    def get_success_url(self):
        return reverse('videos:index')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class VideoCategoryList(View):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        videos = Video.objects.filter(category=pk).order_by('-date_post')
        context = {
            'category': category,
            'videos': videos
        }

        return render(request, 'videos/video_category.html', context)


class SearchVideo(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        query_list = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploader__username__icontains=query)
        )

        context = {
            'query_list': query_list,
        }

        return render(request, 'videos/search.html', context)