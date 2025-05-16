import { Component } from '@angular/core';
import { Book } from '../../Models/book.model'; // book.interface.ts dosyan burada olmalı
import { BookService } from '../../book.service';

@Component({
  selector: 'app-search',
  standalone: false,
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent  {
  query: string = '';
  books: Book[] = [];

  constructor(private bookService: BookService) {}

  onSearch(): void {
    if (!this.query.trim()) return;

    this.bookService.searchBooks(this.query).subscribe((results: Book[]) => {
      this.books = results;
    });
  }
}
