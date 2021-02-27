import unittest
from test_garagesale import GarageSaleTestCase

def suite():
    suite = unittest.TestSuite()
    suite.addTest(GarageSaleTestCase('test_get_saleitems'))
    suite.addTest(GarageSaleTestCase('test_get_saleitem'))
    suite.addTest(GarageSaleTestCase('test_get_saleitem_404'))
    suite.addTest(GarageSaleTestCase('test_post_saleitems'))
    suite.addTest(GarageSaleTestCase('test_patch_saleitem'))
    suite.addTest(GarageSaleTestCase('test_patch_saleitem_error'))
    suite.addTest(GarageSaleTestCase('test_post_saleitems_missing_data'))
    suite.addTest(GarageSaleTestCase('test_buy_item'))
    suite.addTest(GarageSaleTestCase('test_buy_item_missing_userid'))
    suite.addTest(GarageSaleTestCase('test_get_users'))
    suite.addTest(GarageSaleTestCase('test_delete_saleitem_error'))
    suite.addTest(GarageSaleTestCase('test_delete_saleitem'))
    suite.addTest(GarageSaleTestCase('test_get_users_403'))
    suite.addTest(GarageSaleTestCase('test_get_user'))
    suite.addTest(GarageSaleTestCase('test_get_user_404'))
    suite.addTest(GarageSaleTestCase('test_post_users'))
    suite.addTest(GarageSaleTestCase('test_post_users_missing_data'))
    suite.addTest(GarageSaleTestCase('test_patch_user'))
    suite.addTest(GarageSaleTestCase('test_patch_user_error'))
    suite.addTest(GarageSaleTestCase('test_delete_user'))
    suite.addTest(GarageSaleTestCase('test_delete_user_error'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=False)
    runner.run(suite())