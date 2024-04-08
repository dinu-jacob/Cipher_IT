using Steganography;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Drawing.Imaging;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        
        private Bitmap bmp = null;
        private string extractedText = string.Empty;
        public Form1()
        {
            InitializeComponent();
        }
                      

        private void button1_Click(object sender, EventArgs e)
        {
            bmp = (Bitmap)pictureBox1.Image;

            string text = textBox1.Text;

            if (text.Equals(""))
            {
                MessageBox.Show("The text you want to hide can't be empty", "Warning");

                return;
            }

           
            else if (textBox2.Text.Length < 6)
                {
                    MessageBox.Show("Please enter a password with at least 6 characters", "Warning");

                    return;
                }
                else
                {
                    text = Crypto.EncryptStringAES(text, textBox2.Text);
                }
            

            bmp = SteganographyHelper.embedText(text, bmp);

            MessageBox.Show("Your text was hidden in the image successfully!", "Done"); 
            
            string extractedText = SteganographyHelper.extractText(bmp);
            // CRUD.insUpDel("ins_im", extractedText, textBox2.Text, 'w',textBox1.Text);


            
        }
           

        private void imageToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
         
             openFileDialog1.Filter = "Image Files (*.jpeg; *.png; *.bmp)|*.jpg; *.png; *.bmp";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                pictureBox1.Image = Image.FromFile(openFileDialog1.FileName);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            bmp = (Bitmap)pictureBox1.Image;

            string extractedText = SteganographyHelper.extractText(bmp);

           
                try
                {
                    extractedText = Crypto.DecryptStringAES(extractedText, textBox2.Text);
                }
                catch
                {
                    MessageBox.Show("password not entered", "Error");

                    return;
                }
            

            textBox1.Text = extractedText;
        }

        private void saveImageToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog save_dialog = new SaveFileDialog();
            save_dialog.Filter = "Png Image|*.png|Bitmap Image|*.bmp";

            if (save_dialog.ShowDialog() == DialogResult.OK)
            {
                switch (save_dialog.FilterIndex)
                {
                    case 0:
                        {
                            bmp.Save(save_dialog.FileName, ImageFormat.Png);
                        } break;
                    case 1:
                        {
                            bmp.Save(save_dialog.FileName, ImageFormat.Bmp);
                        } break;
                }

              
            }
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
