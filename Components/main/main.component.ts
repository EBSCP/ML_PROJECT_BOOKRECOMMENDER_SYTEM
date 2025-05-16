import { Component, OnInit } from '@angular/core';
import { BookService } from '../../book.service';
import { Book } from '../../Models/book.model';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  standalone:false,
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  books: Book[] = [];
  sortedBooks: Book[] = [];

  constructor(private bookService: BookService) {}
  ngOnInit() {
    this.bookService.getBooks().subscribe((data) => {
      console.log('API Response:', data); // API yanıtını kontrol et

      // Eğer data ve sample_books varsa işle
      if (data && Array.isArray(data.sample_books)) {
        this.books = data.sample_books;
        console.log('Books:', this.books);

        // Yeni bir dizi oluştur ve sıralama işlemini burada yap
        this.sortedBooks = [...this.books].sort((a, b) => {
          return a.Title.localeCompare(b.Title); // Başlık bazında sıralama
        });

        console.log('Sorted Books:', this.sortedBooks);
      } else {
        console.error('Veri formatı hatalı! sample_books dizisi bulunamadı.');
      }
    });
  }


  // Kitapları sıralama
  sortBooks(books: Book[]): Book[] {
    return books.sort((a, b) => {
      return a.Title.localeCompare(b.Title); // Başlık bazında sıralama
    });
  }
}
