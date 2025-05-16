import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BookService {
  private apiUrl = 'http://localhost:8000'; // FastAPI URL'si

  constructor(private http: HttpClient) {}

  // API'den kitap verilerini al
  getBooks(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}`);
  }

  // Arama ve öneri API'si
  searchBooks(query: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/search?q=${query}`);
  }

  recommendBook(bookTitle: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/recommend/${bookTitle}`);
  }
}
