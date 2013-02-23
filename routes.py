# routes.py - maps urls to their handlers

from webapp2 import Route

_routes = [

    # Items
    Route('/items', handler='views.items.Items', name='items', methods=['GET']),
    Route('/items/add', handler='views.items.ItemAdd', name='add', methods=['GET', 'POST']),
    Route('/items/edit/<id:(.+)>', handler='views.items.ItemEdit', name='edit', methods=['GET', 'POST']),
    Route('/items/del/<id:(.+)>', handler='views.items.ItemDel', name='del', methods=['GET', 'POST']),


    #discussions and comments
    Route('/discussions', handler='views.discussions.DiscHome', name='discussions', methods=['GET']),
    Route('/discussions/add', handler='views.discussions.DiscAdd', name='discussions add', methods=['GET', 'POST']),
    Route('/discussions/edit/<d_id:(.+)>', handler='views.discussions.DiscEdit', name='discussions edit', methods=['GET', 'POST']),
    Route('/discussions/view/<d_id:(.+)>', handler='views.discussions.DiscView', name='discussions view', methods=['GET']),
    Route('/discussions/del/<d_id:(.+)>', handler='views.discussions.DiscDel', name='discussions del', methods=['GET']),
    Route('/comments/add/<d_id:(.+)>', handler='views.discussions.CommAdd', name='comments add', methods=['POST']),
    #Route('/comments/edit/<c_id:(.+)>', handler='views.discussions.CommEdit', name='comments edit', methods=['GET', 'POST']),
    Route('/comments/del/<c_id:(.+)>', handler='views.discussions.CommDel', name='comments del', methods=['GET']),

    # Admin
    Route('/admin/enable/<id:(.+)>', handler='views.admin.AdminEnable', name='enable', methods=['GET']),
    Route('/admin/disable/<id:(.+)>', handler='views.admin.AdminDisable', name='disable', methods=['GET']),
    Route('/admin/remove_admin/<id:(.+)>', handler='views.admin.AdminRemove', name='remove_admin', methods=['GET']),    
    Route('/admin/make_admin/<id:(.+)>', handler='views.admin.AdminAdd', name='make_admin', methods=['GET']),
    Route('/admin/del/item/<id:(.+)>', handler='views.admin.AdminRemoveItemHandler', name='admin_item_remove', methods=['GET', 'POST']),
    Route('/admin', handler='views.admin.AdminHandler', name='admin', methods=['GET']),
    Route('/superadmin', handler='views.admin.SuperAdminHandler', name='superadmin', methods=['GET']),
    Route('/superadmin/signout', handler='views.admin.SuperAdminSignOut', name='superadmin_signout', methods=['GET']),
    
    # User auth
    Route('/quit', handler='views.user_auth.RemoveAccountHandler', name='quit', methods=['GET']),
    Route('/profile/<id:.+>', handler='views.user_auth.ProfileHandler', name='profile', methods=['GET']),
    Route('/profile', handler='views.user_auth.ProfileHandler', name='profile', methods=['GET']),
    Route('/signout', handler='views.user_auth.SignOutHandler', name='signout', methods=['GET']),
    Route('/signin', handler='views.user_auth.SignInHandler', name='signin', methods=['GET','POST']),
	Route('/signup', handler='views.user_auth.SignUpHandler', name='signup', methods=['GET', 'POST']),
	Route('/v/<token:.+>', handler='views.user_auth.VerificationHandler', name='verify', methods=['GET']),
	
	# Home
	Route('/home', handler='views.home.HomeHandler', name='home', methods=['GET']),
    Route('/', handler='views.home.HomeHandler', name='home', methods=['GET']),
	Route('/browse', handler='views.search.Browse', name='search', methods=['GET']),
    Route('/search', handler='views.search.Search', name='search', methods=['GET']),
]


def get_routes():
    return _routes
