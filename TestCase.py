import unittest
from tkinter import Tk, Text, Entry, Label
from Final import showimage, Hide, Show, save, refresh
from stegano import lsb
import os

class TestCodeCryptApp(unittest.TestCase):

    def setUp(self):
        # Setup Tkinter root and components before each test
        self.root = Tk()
        self.filename = "images1.png"
        
        # Create dummy Tkinter widgets for testing
        self.text1 = Text(self.root)
        self.email_entry = Entry(self.root)
        self.lbl = Label(self.root)

        # Simulate setting up a filename for testing
        global filename
        filename = self.filename

    def test_showimage(self):
        # Test to ensure showimage function updates filename and loads image
        showimage()
        self.assertTrue('filename' in globals())
        self.assertTrue(filename.endswith(('.jpg', '.png')))

    def test_hide_message(self):
        # Simulate a case of hiding a message inside an image
        global filename
        filename = self.filename  
        secret_message = "This is a secret message"
        
        self.text1.insert(1.0, secret_message)
        self.email_entry.insert(0, "test@example.com")
        
        Hide()
        
        # Verify that the message was hidden in the image
        hidden_image_path = filename.split(".")[0] + "_hidden.png"
        self.assertTrue(os.path.exists(hidden_image_path))
        
        # Check that the message is hidden and success message is shown
        self.assertIn("Data hidden successfully!", self.text1.get(1.0, "end").strip())

    def test_show_hidden_message(self):
        # Test to ensure hidden message is revealed correctly
        global filename
        filename = self.filename  
        secret = lsb.hide(filename, "This is a hidden message")
        secret.save(filename)  

        Show()

        # Verify the hidden message is displayed correctly
        self.assertIn("This is a hidden message", self.text1.get(1.0, "end").strip())

    def test_show_no_hidden_message(self):
        # Test to ensure no hidden message gives the correct response
        global filename
        filename = self.filename  

        Show()

        self.assertIn("No hidden message found in the image.", self.text1.get(1.0, "end").strip())

    def test_save_image(self):
        # Test to ensure the image is saved after hiding data
        global filename
        filename = self.filename  

        Hide()  # Assume hide is called to save an image
        save()

        hidden_image_path = filename.split(".")[0] + "_hidden.png"
        self.assertTrue(os.path.exists(hidden_image_path))

    def test_refresh_function(self):
        # Test the refresh function to ensure UI components are reset
        self.text1.insert(1.0, "Sample text")
        self.email_entry.insert(0, "test@example.com")
        global filename
        filename = "test_image.png"
        self.lbl.config(image="some_image")
        
        # Call refresh
        refresh()
        
        # Check that the UI components are reset correctly
        self.assertEqual(self.text1.get(1.0, "end").strip(), "")
        self.assertEqual(self.email_entry.get(), "")
        self.assertIsNone(self.lbl.image)

    def tearDown(self):
        # Destroy root after each test
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()
