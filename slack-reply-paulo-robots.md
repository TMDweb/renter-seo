Hi Paulo, thanks 🙏 Just to clarify the nature of these PRs: they're specs, the SEO requirements for robots and the sitemap. I didn't change, touch, or remove anything you built, each PR just adds one new file as a reference for you to review and apply your way.

So you're free to own the file and the merge. The two things I'd ask you to keep from PR #1:

1. **Disallow rules instead of `allow: "/"`** so Google doesn't crawl/index the private and transactional pages (profile, chat, booking, payment, item management, search).
2. **Two sitemaps (`/sitemap/ar.xml`, `/sitemap/en.xml`), not `/sitemap.xml`** that single URL would 404 since the sitemap generates per-language files.

Lift those into your file and we're aligned. Happy to call. Thanks!
