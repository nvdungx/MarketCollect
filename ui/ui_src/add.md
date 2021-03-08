        import os
        
        application_path = os.path.dirname(__file__)
        self.uidir = os.path.abspath(os.path.join(application_path, "../."))

        (u"icons.*")
        os.path.join(self.uidir, $1)