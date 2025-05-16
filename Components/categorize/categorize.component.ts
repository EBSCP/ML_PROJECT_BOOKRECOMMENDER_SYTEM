import { Component } from '@angular/core';
import { Book } from '../../Models/book.model';
import { BookService } from '../../book.service';

@Component({
  selector: 'app-categorize',
  standalone: false,
  templateUrl: './categorize.component.html',
  styleUrl: './categorize.component.css'
})
export class CategorizeComponent   {
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
