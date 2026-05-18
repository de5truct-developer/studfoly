/* ============================================================
   СТУДФОЛИО — Main JavaScript
   Multi-user student portfolio platform
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    /* ---- AOS Initialization ---- */
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 600,
            easing: 'ease-out-cubic',
            once: true,
            offset: 60,
        });
    }

    /* ============================================================
       THEME TOGGLE
       ============================================================ */
    var themeToggle = document.getElementById('themeToggle');
    var body = document.body;

    // Initialize theme from localStorage or body attribute
    var savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.setAttribute('data-theme', savedTheme);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var current = body.getAttribute('data-theme') || 'light';
            var newTheme = current === 'light' ? 'dark' : 'light';
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            // If authenticated, save to server
            if (typeof IS_AUTHENTICATED !== 'undefined' && IS_AUTHENTICATED) {
                fetch('/accounts/toggle-theme/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'theme=' + newTheme,
                }).catch(function () {});
            }
        });
    }

    /* ============================================================
       NAVBAR — scroll effect & mobile toggle
       ============================================================ */
    var navbar = document.getElementById('navbar');
    var navToggle = document.getElementById('navToggle');
    var navMenu = document.getElementById('navMenu');

    function handleNavbarScroll() {
        if (!navbar) return;
        if (window.scrollY > 30) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    window.addEventListener('scroll', handleNavbarScroll);
    handleNavbarScroll();

    // Mobile toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('open');
        });

        // Close on link click
        navMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navToggle.classList.remove('active');
                navMenu.classList.remove('open');
            });
        });
    }

    // Close menu on outside click
    document.addEventListener('click', function (e) {
        if (navMenu && navToggle && navMenu.classList.contains('open')) {
            if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('open');
            }
        }
    });

    /* ============================================================
       PROFILE DROPDOWN
       ============================================================ */
    var dropdownToggle = document.getElementById('profileDropdownToggle');
    var dropdownMenu = document.getElementById('profileDropdownMenu');
    var navDropdown = dropdownToggle ? dropdownToggle.closest('.nav-dropdown') : null;

    if (dropdownToggle && navDropdown) {
        dropdownToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            navDropdown.classList.toggle('open');
        });

        document.addEventListener('click', function (e) {
            if (!navDropdown.contains(e.target)) {
                navDropdown.classList.remove('open');
            }
        });
    }

    /* ============================================================
       BACK TO TOP
       ============================================================ */
    var backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 400) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* ============================================================
       TOAST AUTO-CLOSE
       ============================================================ */
    document.querySelectorAll('.toast[data-auto-close]').forEach(function (toast) {
        var delay = parseInt(toast.getAttribute('data-auto-close'), 10) || 5000;
        setTimeout(function () {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(30px)';
            setTimeout(function () { toast.remove(); }, 300);
        }, delay);
    });

    /* ============================================================
       TABS
       ============================================================ */
    document.querySelectorAll('.tab-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var tabId = btn.getAttribute('data-tab');
            var parent = btn.closest('.edit-form') || document;

            // Deactivate all tabs
            parent.querySelectorAll('.tab-btn').forEach(function (b) { b.classList.remove('active'); });
            parent.querySelectorAll('.tab-content').forEach(function (c) { c.classList.remove('active'); });

            // Activate selected
            btn.classList.add('active');
            var target = parent.querySelector('#tab-' + tabId);
            if (target) target.classList.add('active');
        });
    });

    /* ============================================================
       SKILL BARS ANIMATION
       ============================================================ */
    var skillBarsAnimated = false;

    function animateSkillBars() {
        if (skillBarsAnimated) return;
        var fills = document.querySelectorAll('.skill-bar-fill-mini');
        if (fills.length === 0) return;

        var firstFill = fills[0];
        var rect = firstFill.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            skillBarsAnimated = true;
            fills.forEach(function (fill) {
                var pct = fill.getAttribute('data-percentage');
                if (pct) {
                    setTimeout(function () {
                        fill.style.width = pct + '%';
                    }, 200);
                }
            });
        }
    }
    window.addEventListener('scroll', animateSkillBars);
    animateSkillBars();

    /* ============================================================
       LIKE TOGGLE
       ============================================================ */
    var likeBtn = document.getElementById('likeBtn');
    if (likeBtn) {
        likeBtn.addEventListener('click', function () {
            var projectId = likeBtn.getAttribute('data-project-id');
            fetch('/interactions/like/toggle/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'project_id=' + projectId,
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.status === 'ok') {
                    var icon = likeBtn.querySelector('i');
                    var count = document.getElementById('likesCount');
                    if (data.liked) {
                        likeBtn.classList.add('active');
                        icon.className = 'fa-solid fa-heart';
                    } else {
                        likeBtn.classList.remove('active');
                        icon.className = 'fa-regular fa-heart';
                    }
                    if (count) count.textContent = data.likes_count;
                }
            })
            .catch(function () {});
        });
    }

    /* ============================================================
       BOOKMARK TOGGLE
       ============================================================ */
    var bookmarkBtn = document.getElementById('bookmarkBtn');
    if (bookmarkBtn) {
        bookmarkBtn.addEventListener('click', function () {
            var projectId = bookmarkBtn.getAttribute('data-project-id');
            fetch('/interactions/bookmark/toggle/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'project_id=' + projectId,
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.status === 'ok') {
                    var icon = bookmarkBtn.querySelector('i');
                    if (data.bookmarked) {
                        bookmarkBtn.classList.add('active');
                        icon.className = 'fa-solid fa-bookmark';
                    } else {
                        bookmarkBtn.classList.remove('active');
                        icon.className = 'fa-regular fa-bookmark';
                    }
                }
            })
            .catch(function () {});
        });
    }

    /* ============================================================
       COMMENTS
       ============================================================ */
    var commentForm = document.getElementById('commentForm');
    var commentsList = document.getElementById('commentsList');

    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var formData = new FormData(commentForm);

            fetch('/interactions/comment/add/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                },
                body: formData,
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.status === 'ok') {
                    var c = data.comment;
                    var avatarHtml = c.avatar_url
                        ? '<img src="' + c.avatar_url + '" alt="" class="comment-avatar">'
                        : '<div class="comment-avatar-placeholder"><i class="fa-solid fa-user"></i></div>';

                    var html = '<div class="comment" id="comment-' + c.id + '">'
                        + '<div class="comment-header">'
                        + avatarHtml
                        + '<div class="comment-meta">'
                        + '<a href="/accounts/profile/' + c.username + '/" class="comment-author">' + c.user + '</a>'
                        + '<span class="comment-date">только что</span>'
                        + '</div>'
                        + '<button class="comment-delete-btn" data-comment-id="' + c.id + '" title="Удалить">'
                        + '<i class="fa-solid fa-trash"></i></button>'
                        + '</div>'
                        + '<p class="comment-text">' + escapeHtml(c.text) + '</p>'
                        + '</div>';

                    // Remove "no comments" message
                    var emptyMsg = commentsList.querySelector('.comments-empty');
                    if (emptyMsg) emptyMsg.remove();

                    if (c.parent_id) {
                        var parentComment = document.getElementById('comment-' + c.parent_id);
                        if (parentComment) {
                            var repliesDiv = parentComment.querySelector('.comment-replies');
                            if (!repliesDiv) {
                                repliesDiv = document.createElement('div');
                                repliesDiv.className = 'comment-replies';
                                parentComment.appendChild(repliesDiv);
                            }
                            repliesDiv.insertAdjacentHTML('beforeend', html.replace('class="comment"', 'class="comment reply"'));
                        }
                    } else {
                        commentsList.insertAdjacentHTML('afterbegin', html);
                    }

                    commentForm.querySelector('textarea').value = '';
                    // Remove reply hidden field if exists
                    var parentInput = commentForm.querySelector('input[name="parent_id"]');
                    if (parentInput) parentInput.remove();
                    var replyIndicator = commentForm.querySelector('.reply-indicator');
                    if (replyIndicator) replyIndicator.remove();

                    bindCommentEvents();
                }
            })
            .catch(function () {});
        });
    }

    function bindCommentEvents() {
        // Delete comment
        document.querySelectorAll('.comment-delete-btn').forEach(function (btn) {
            btn.onclick = function () {
                if (!confirm('Удалить комментарий?')) return;
                var commentId = btn.getAttribute('data-comment-id');
                fetch('/interactions/comment/delete/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'comment_id=' + commentId,
                })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.status === 'ok') {
                        var commentEl = document.getElementById('comment-' + commentId);
                        if (commentEl) commentEl.remove();
                    }
                })
                .catch(function () {});
            };
        });

        // Reply
        document.querySelectorAll('.comment-reply-btn').forEach(function (btn) {
            btn.onclick = function () {
                if (!commentForm) return;
                var commentId = btn.getAttribute('data-comment-id');

                // Remove existing parent_id input and indicator
                var existing = commentForm.querySelector('input[name="parent_id"]');
                if (existing) existing.remove();
                var existingIndicator = commentForm.querySelector('.reply-indicator');
                if (existingIndicator) existingIndicator.remove();

                // Add parent_id
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'parent_id';
                input.value = commentId;
                commentForm.appendChild(input);

                // Add indicator
                var indicator = document.createElement('div');
                indicator.className = 'reply-indicator';
                indicator.innerHTML = '<small style="color:var(--text-muted);">Ответ на комментарий <button type="button" onclick="this.parentElement.parentElement.querySelector(\'input[name=parent_id]\').remove(); this.parentElement.remove();" style="background:none;border:none;color:var(--danger);cursor:pointer;font-size:0.85rem;">Отмена</button></small>';
                commentForm.querySelector('.comment-form-body').before(indicator);

                commentForm.querySelector('textarea').focus();
            };
        });
    }
    bindCommentEvents();

    /* ============================================================
       CHAT / MESSAGING
       ============================================================ */
    var chatForm = document.getElementById('chatForm');
    var chatMessages = document.getElementById('chatMessages');
    var chatInput = document.getElementById('chatInput');

    if (chatForm && chatMessages) {
        // Scroll to bottom on load
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Auto-resize textarea
        if (chatInput) {
            chatInput.addEventListener('input', function () {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            });

            // Send on Enter (without Shift)
            chatInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    chatForm.dispatchEvent(new Event('submit'));
                }
            });
        }

        // Send message
        chatForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var text = chatInput.value.trim();
            if (!text) return;

            var formData = new FormData(chatForm);

            fetch('/messages/send/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN,
                },
                body: formData,
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.status === 'ok') {
                    appendMessage(data.message, true);
                    chatInput.value = '';
                    chatInput.style.height = 'auto';
                }
            })
            .catch(function () {});
        });

        // Poll for new messages
        var conversationId = chatMessages.getAttribute('data-conversation-id');
        if (conversationId) {
            setInterval(function () {
                var allMsgs = chatMessages.querySelectorAll('.chat-message');
                var lastId = 0;
                if (allMsgs.length > 0) {
                    lastId = allMsgs[allMsgs.length - 1].getAttribute('data-message-id') || 0;
                }

                fetch('/messages/check-new/?conversation_id=' + conversationId + '&last_id=' + lastId, {
                    headers: { 'X-CSRFToken': CSRF_TOKEN },
                })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.status === 'ok' && data.messages && data.messages.length > 0) {
                        data.messages.forEach(function (msg) {
                            appendMessage(msg, false);
                        });
                    }
                })
                .catch(function () {});
            }, 5000);
        }
    }

    function appendMessage(msg, isSent) {
        if (!chatMessages) return;
        var cls = isSent ? 'sent' : 'received';
        var avatarHtml = '';
        if (!isSent) {
            if (msg.avatar_url) {
                avatarHtml = '<div class="chat-message-avatar"><img src="' + msg.avatar_url + '" alt=""></div>';
            } else {
                avatarHtml = '<div class="chat-message-avatar"><div class="chat-msg-avatar-placeholder"><i class="fa-solid fa-user"></i></div></div>';
            }
        }

        var html = '<div class="chat-message ' + cls + '" data-message-id="' + msg.id + '">'
            + avatarHtml
            + '<div class="chat-message-bubble">'
            + '<p>' + escapeHtml(msg.text) + '</p>'
            + '<span class="chat-message-time">' + msg.created_at + '</span>'
            + '</div></div>';

        chatMessages.insertAdjacentHTML('beforeend', html);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    /* ============================================================
       UNREAD MESSAGE COUNT POLLING
       ============================================================ */
    if (typeof IS_AUTHENTICATED !== 'undefined' && IS_AUTHENTICATED) {
        setInterval(function () {
            fetch('/messages/unread-count/', {
                headers: { 'X-CSRFToken': CSRF_TOKEN },
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                var badge = document.getElementById('navUnreadBadge');
                if (data.unread_count > 0) {
                    if (badge) {
                        badge.textContent = data.unread_count;
                    } else {
                        var msgLink = document.querySelector('.nav-link-messages');
                        if (msgLink) {
                            var newBadge = document.createElement('span');
                            newBadge.className = 'nav-badge';
                            newBadge.id = 'navUnreadBadge';
                            newBadge.textContent = data.unread_count;
                            msgLink.appendChild(newBadge);
                        }
                    }
                } else {
                    if (badge) badge.remove();
                }
            })
            .catch(function () {});
        }, 30000);
    }

    /* ============================================================
       IMAGE PREVIEW ON FILE INPUT
       ============================================================ */
    document.querySelectorAll('input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                var previewId = 'avatarPreview';
                var preview = document.getElementById(previewId);
                reader.onload = function (e) {
                    if (preview) {
                        if (preview.tagName === 'IMG') {
                            preview.src = e.target.result;
                        } else {
                            // Replace placeholder with img
                            var img = document.createElement('img');
                            img.src = e.target.result;
                            img.className = 'avatar-preview';
                            img.id = previewId;
                            preview.parentNode.replaceChild(img, preview);
                        }
                    }
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    /* ============================================================
       SEARCH DEBOUNCE (Home page)
       ============================================================ */
    var searchInput = document.getElementById('searchInput');
    var searchForm = document.getElementById('searchForm');
    var searchTimeout = null;

    if (searchInput && searchForm) {
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function () {
                // Don't auto-submit, just set a visual indicator
                // User will submit manually or on enter
            }, 300);
        });
    }

    /* ============================================================
       SMOOTH SCROLLING
       ============================================================ */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var targetId = this.getAttribute('href');
            if (targetId === '#') return;
            var target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                var offset = navbar ? navbar.offsetHeight : 0;
                var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
            }
        });
    });

    /* ============================================================
       UTILITY: Escape HTML
       ============================================================ */
    function escapeHtml(text) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }
});
